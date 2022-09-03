
from contextlib import nullcontext
import datetime
import threading
import json
from tkinter import NONE
from types import NoneType
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt

from MemberSystem.models import *
from Club.models import *

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
                    action = Action.objects.get(user=user, target=contractAddress, action_type="join")
                    Participant.objects.create(
                                            plan=plan,
                                            user=user,
                                            tokens=amount,
                                            role="風險供給者",
                                            join_date=action.request_time,
                                            take_effect_date=action.act_time)
                    action.done=True
                    action.save()
            
            actions = Action.objects.filter(target=contractAddress, action_type="join", done=False)
            for action in actions:
                plan = Plan.objects.get(contract_address=action.target)
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
    waitForIssue = Action.objects.values('target').filter(
        action_type='join', done=False, tx_hash__isnull=True).annotate(count=Count('target'))
    waitForTXComplete = Action.objects.values('target').filter(
        action_type='join', done=False, tx_hash__isnull=False).annotate(count=Count('target'))
    context = {
        'waitForIssue': waitForIssue,
        'waitForTXComplete': waitForTXComplete,
    }
    test = Action.objects.get(target="0x85318e8aD65140b10177Db877F083e785283A450")
    return render(request, 'dashboard.html', context)

@csrf_exempt
def tokenIssue(request, target):
    toDo = Action.objects.filter(done=False, action_type="join", target=target)
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

def issueSucceed(request):
    if request.POST:
        txHash = request.POST.get("txHash")