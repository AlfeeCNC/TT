
from contextlib import nullcontext
import datetime
import threading
import json
from types import NoneType
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.views.decorators.csrf import csrf_exempt


from MemberSystem.models import *
from Club.models import *
from MemberSystem.views import *
import TriggerToken.ethereum as TTethereum

import web3
from web3 import Web3
from eth_account.messages import encode_defunct

# Infura Node
InfuraURL = "https://ropsten.infura.io/v3/ed00ddb25c3b460c9b99f2375a314102"
# Initiating Web3
web3 = Web3(web3.HTTPProvider(InfuraURL))

# Create your views here.
class IssueReceiptThread(threading.Thread):

    def __init__(self, txHash):
        self.txHash = txHash
        threading.Thread.__init__(self)

    def run(self):
        print("Strat issueToken threading....")
        try:
            receipt = web3.eth.wait_for_transaction_receipt(self.txHash)
            print("Get transaction receipt...., writing some data into DB.....")
            sharedAddress = web3.toChecksumAddress("0xac0868B1DcA15532d7EaCF8fA1eE5bcae0300D1A")
            for log in receipt.logs:
                
                # log.topics[1] 可以看到實際接收地址，就是使用者帳號
                userAddress = web3.toChecksumAddress("0x"+log.topics[2].hex()[-40:])
                # log.data 是移轉的數目
                amount = int(log.data, 16)//1000000000000000000
                # log.address 是合約地址
                contractAddress = web3.toChecksumAddress(log.address)

                if userAddress == sharedAddress:
                    pass
                else:
                    user = User.objects.get(username = userAddress)
                    plan = Plan.objects.get(contract_address = contractAddress)
                    action = Action.objects.get(user=user, target=plan, action_type="join", done=False)
                    Participant.objects.create(
                                            plan=plan,
                                            user=user,
                                            tokens=amount,
                                            role="風險供給者",
                                            join_date=action.request_time,
                                            take_effect_date=action.act_time)
                    action.done=True
                    action.save()
                plan = Plan.objects.get(contract_address = contractAddress)
                actions = Action.objects.filter(target=plan, action_type="join", done=False)
                for action in actions:
                    plan = action.target
                    user = action.user
                    amount = action.amount
                    Participant.objects.create(
                                            plan=plan,
                                            user=user,
                                            tokens=amount,
                                            role="風險供給者",
                                            join_date=action.request_time,
                                            take_effect_date=action.act_time)
                    action.done=True
                    action.save()
        except Exception as e:
            print(e)
class BurnReceiptThread(threading.Thread):

    def __init__(self, txHash, taskID):
        self.txHash = txHash
        self.taskID = taskID
        threading.Thread.__init__(self)

    def run(self):
        print("Strat BurnToken threading....")
        try:
            receipt = web3.eth.wait_for_transaction_receipt(self.txHash)
            print("Get transaction receipt...., writing some data into DB.....")
            sharedAddress = web3.toChecksumAddress("0xac0868B1DcA15532d7EaCF8fA1eE5bcae0300D1A")
            for log in receipt.logs:
                amount = int(log.data, 16)//1000000000000000000
                action = Action.objects.get(id=self.taskID)
                user = action.user
                plan = action.target
                action.done=True
                action.save()
                try:
                    participant = Participant.objects.get(plan=plan, user=user)
                    participant.tokens -= amount
                    participant.save()
                except:
                    pass
            transferCashPoint(user, amount)
        except Exception as e:
            print(e)
class ClaimReceiptThread(threading.Thread):

    def __init__(self, txHash, taskID):
        self.txHash = txHash
        self.taskID = taskID
        threading.Thread.__init__(self)

    def run(self):
        print("Strat Claim threading....")
        try:
            receipt = web3.eth.wait_for_transaction_receipt(self.txHash)
            print("Get transaction receipt...., writing some data into DB.....")
            sharedAddress = web3.toChecksumAddress("0xac0868B1DcA15532d7EaCF8fA1eE5bcae0300D1A")
            for log in receipt.logs:
                amount = int(log.data, 16)//1000000000000000000
                action = Action.objects.get(id=self.taskID)
                user = action.user
                plan = action.target
                action.amount = amount
                action.done=True
                action.save()

            if action.action_type == "claimThenBurn":
                burnAction=Action(
                    user = user,
                    action_type = "quit",
                    target = plan,
                    amount = amount,
                    request_time = datetime.datetime.now(),
                    act_time = datetime.datetime.now(),
                    done = False
                )
                burnAction.save()
            else :
                pass
        except Exception as e:
            print(e)
def adminLogin(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username is not None:
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active and user.is_staff:
                auth.login(request, user)
                return redirect(reverse_lazy('adminDashboard'))
            else:
                hasError = True
                context = {
                    'hasError': hasError
                }
                return render(request, 'login.html', context)
    return render(request, 'login.html')


def adminDashboard(request):
    # waitForIssue = Action.objects.filter(action_type='join', done=False, tx_hash__isnull=True).annotate(count=Count('target'))
    waitForIssue = Action.objects.values('target').filter(action_type='join', done=False, tx_hash__isnull=True).annotate(count=Count('target'))
    waitForBurn = Action.objects.filter(Q(action_type='payment')|Q(action_type='quit')|Q(action_type="decrease"), done=False, tx_hash__isnull=True)
    waitForIssueComplete = Action.objects.filter(action_type='join', done=False, tx_hash__isnull=False).annotate(count=Count('target'))
    waitForBurnComplete = Action.objects.filter(Q(action_type='payment')|Q(action_type='quit')|Q(action_type="decrease"), done=False, tx_hash__isnull=False)
    waitForWhitelist = UserInfo.objects.values('is_whitelist').filter(is_whitelist=False).annotate(count=Count('is_whitelist'))
    waitForClaim = Action.objects.filter(Q(action_type='claimThenBurn')|Q(action_type='claim'), done=False, tx_hash__isnull=True)
    waitForClaimComplete = Action.objects.filter(Q(action_type='claimThenBurn')|Q(action_type='claim'), done=False, tx_hash__isnull=False)
    context = {
        'waitForIssue': waitForIssue,
        'waitForBurn' : waitForBurn,
        'waitForWhitelist' : waitForWhitelist,
        'waitForClaim' : waitForClaim,
        'waitForIssueComplete': waitForIssueComplete,
        'waitForBurnComplete': waitForBurnComplete,
        'waitForClaimComplete' : waitForClaimComplete,
    }
    try:
        for task in waitForIssue:
            plan = Plan.objects.get(id=task['target'])
            task['target'] = plan.contract_address
    except:
        pass
    try:
        for task in waitForBurnComplete:
            plan = Plan.objects.get(id=task['target'])
            task['target'] = plan.contract_address
    except:
        pass
    return render(request, 'dashboard.html', context)

@csrf_exempt
def tokenIssue(request, target):
    plan = Plan.objects.get(contract_address=target)
    targetID = plan.id
    toDo = Action.objects.filter(done=False, action_type="join", target=targetID)
    sharedAddress = web3.toChecksumAddress("0xac0868B1DcA15532d7EaCF8fA1eE5bcae0300D1A")
    mintDict = {}
    count = 0
    for task in toDo:
        try:
            if task.user.username == web3.toChecksumAddress(task.user.username):
                address = task.user.username
                mintDict[address] = task.amount*1000000000000000000
        except:
            count += task.amount
    if count != 0:
        mintDict[sharedAddress] = count*1000000000000000000
    
    context = {
        "toDo": toDo,
        "mintDict": json.dumps(mintDict),
        "address": target,
    }

    if request.POST:
        txHash = request.POST.get("txHash")
        toDo.update(tx_hash=txHash)
        receiptThread = IssueReceiptThread(txHash)
        receiptThread.start()
        return redirect(reverse_lazy('adminDashboard'))
    return render(request, 'tokenIssue.html', context)


@csrf_exempt
def tokenBurn(request, target, user, taskID):
    user = User.objects.get(username=user)
    plan = Plan.objects.get(id=target)
    participanting = Participant.objects.get(plan=plan, user=user)
    task = Action.objects.get(id = taskID)
    sharedAddress = web3.toChecksumAddress("0xac0868B1DcA15532d7EaCF8fA1eE5bcae0300D1A")
    burnDict = {}
    try:
        if task.user.username == web3.toChecksumAddress(task.user.username):
            userAddress = task.user.username
    except:
        userAddress = sharedAddress
    burnDict['account'] = userAddress
    burnDict['amount'] = task.amount * 1000000000000000000
    context = {
        "task" : task,
        "burnDict" : burnDict
    }
    if request.POST:
        txHash = request.POST.get("txHash")
        task.tx_hash=txHash
        task.save()
        if task.action_type == "quit":
            participanting.delete()
        
        receiptThread = BurnReceiptThread(txHash, taskID)
        receiptThread.start()
        
        return redirect(reverse_lazy('adminDashboard'))
    return render(request, 'tokenBurn.html', context)

def transferCashPoint(user, amount):
    userInfo = UserInfo.objects.get(user=user)
    recipient = userInfo.wallet_address
    amount = int(amount*10000)
    nonce = web3.eth.getTransactionCount(TTethereum.developerPublicKey)

    txn = TTethereum.cashPointContract.functions.transfer(recipient, amount).buildTransaction({
            'chainId': 3,
            'from': TTethereum.developerPublicKey,
            'gas': 370000,
            'gasPrice': web3.eth.gas_price,
            'nonce': nonce
        })
    signed_txn = web3.eth.account.signTransaction(
            txn, private_key=TTethereum.developerPrivateKey)
    txHash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    receiptThread = BuyCashPointReceiptThread(txHash, recipient, user.username)
    receiptThread.start()

@csrf_exempt
def setWhitelist(request):
    tasks = UserInfo.objects.filter(is_whitelist=False)
    sharedAddress = web3.toChecksumAddress("0xac0868B1DcA15532d7EaCF8fA1eE5bcae0300D1A")
    whitelistDict = {}
    for task in tasks:
        userAddress = task.wallet_address
        if userAddress == sharedAddress:
            pass
        else:
            whitelistDict[userAddress] = "True"
    context = {
        'tasks' : tasks,
        'whitelistDict' : whitelistDict,
    }
    if request.POST:
        txHash = request.POST.get("txHash")
        for task in tasks:
            task.is_whitelist = True
            task.save()
        return redirect(reverse_lazy('adminDashboard'))
    return render(request, 'setWhitelist.html', context)

@csrf_exempt
def claim(request, target, user, taskID):
    plan = Plan.objects.get(id=target)
    user = User.objects.get(username=user)
    userInfo = UserInfo.objects.get(user=user)
    userAddress = userInfo.wallet_address
    task = Action.objects.get(id=taskID)
    claimDict={}
    claimDict['account'] = userAddress
    context={
        'task' : task,
        'claimDict' : claimDict
    }
    if request.POST:
        txHash = request.POST.get('txHash')
        task.tx_hash=txHash
        task.save()
        receiptThread = ClaimReceiptThread(txHash, taskID)
        receiptThread.start()
        return redirect(reverse_lazy('adminDashboard'))

    return render(request, 'makeClaim.html', context)