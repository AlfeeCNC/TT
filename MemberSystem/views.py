import math
import secrets
import requests
import json
import threading
import datetime

from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import loader
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.db.models import Count, Q
from django.views.decorators.csrf import csrf_exempt

import web3
from web3 import Web3
from eth_account.messages import encode_defunct

from Club.models import *
from .models import *
from .ecpay_order import cashPointOrder
import TriggerToken.ethereum as TTethereum

# Infura Node
InfuraURL = "https://ropsten.infura.io/v3/ed00ddb25c3b460c9b99f2375a314102"
# Initiating Web3
web3 = Web3(web3.HTTPProvider(InfuraURL))

# Create your views here.


class BuyCashPointReceiptThread(threading.Thread):

    def __init__(self, txHash, useraddress, username):
        self.txHash = txHash
        self.useraddress = useraddress
        self.username = username
        threading.Thread.__init__(self)

    def run(self):
        print("Strat BuyCashPoint threading....")
        try:
            receipt = web3.eth.wait_for_transaction_receipt(self.txHash)
            print("Get transaction receipt...., writing some data into DB.....")
            for log in receipt.logs:
                # log.data 是移轉的數目
                amount = int(log.data, 16)
            print(self.username)
            user = User.objects.get(username=self.username)
            userInfo = UserInfo.objects.get(user=user)
            userInfo.cash_points += amount
            userInfo.save()
        except Exception as e:
            print(e)

class TransferCashPointReceiptThread(threading.Thread):

    def __init__(self, txHash, username):
        self.txHash = txHash
        self.username = username
        threading.Thread.__init__(self)

    def run(self):
        print("Strat TransferCashPoint threading....")
        try:
            receipt = web3.eth.wait_for_transaction_receipt(self.txHash)
            print("Get transaction receipt...., writing some data into DB.....")
            sharedAddress = web3.toChecksumAddress("0xac0868B1DcA15532d7EaCF8fA1eE5bcae0300D1A")
            log = receipt.logs[0]
                # log.data 是移轉的數目
            amount = int(log.data, 16)
            user = User.objects.get(username=self.username)
            userInfo = UserInfo.objects.get(user=user)
            userInfo.cash_points -= amount
            userInfo.save()
        except Exception as e:
            print(e)


def myPortfolio(request):
    user = request.user
    userInfo = UserInfo.objects.get(user=user)
    cashPoint = userInfo.cash_points
    cashPoint = (format(cashPoint, ',d'))
    participating = Participant.objects.all().filter(user=user, quitting=False)
    for p in participating:
        plan = p.plan
        try:
            actions = Action.objects.filter(action_type='decrease', user=user, target=plan, done=False)
            decreaseAmount = 0
            for action in actions:
                decreaseAmount += action.amount
        except:
            decreaseAmount = 0

        try:
            claims = Action.objects.filter(Q(action_type='claim')|Q(action_type='claimThenBurn'), done=True)
            claimAmount = 0
            for claim in claims:
                claimAmount += claim.amount
        except:
            claimAmount = 0

        requestURL = "https://ttdapplet.skychainnet.com/api/supply"
        requestData = {
            "domain": "skychainnet.com",
            "domain_password": "skychain",
            "tt_address": plan.contract_address
        }
        tokenSupplyAPI = requests.post(requestURL, json=requestData)
        response = json.loads(tokenSupplyAPI.content)
        supply = int(response['supply'])//1000000000000000000
        needToPay = round(claimAmount* 10000 / supply * p.tokens)
        nextPeriodAmount = p.tokens - decreaseAmount
        p.needToPay = (format(needToPay, ',d'))
        p.nextPeriodAmount = nextPeriodAmount
    try:
        for claim in claims:
            claimAmount += claim.amount
    except:
        claimAmount = 0
    joinActions = Action.objects.filter(user=user, action_type="join", done=False)
    quitActions = Action.objects.filter(user=user, action_type="quit", done=False)
    context = {
        'cashPoint': cashPoint,
        'participating': participating,
        'joinActions': joinActions,
        'quitActions': quitActions,
    }
    return render(request, 'userDashboard/portfolio.html', context)


def register(request):
    # 已登入直接跳轉
    # if request.user.is_authenticated():
    #     return redirect(reverse_lazy('mutualClubs'))
    sharedAddress = web3.toChecksumAddress(
        "0xac0868B1DcA15532d7EaCF8fA1eE5bcae0300D1A")
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        userWallet = ""
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user:
            return redirect(reverse_lazy('usernameExisted'))
        else:
            User.objects.create(
                username=username,
                password=password,
                email=email
            )
            try:
                if (username == web3.toChecksumAddress(username)):
                    userWallet = username
                else:
                    userWallet = sharedAddress
            except:
                userWallet = sharedAddress
            user = User.objects.get(username=username)
            UserInfo.objects.create(
                user=user,
                name="陳小明",
                birthday=datetime.date.today(),
                ID_number="F123456789",
                bank_account="000128415259322",
                wallet_address=userWallet,
                cash_points=0

            )
            return redirect(reverse_lazy('registerSucceed'))

    context = {
    }
    return render(request, 'register/register.html', context)


def usernameExisted(request):
    return render(request, 'register/usernameExisted.html')


def registerSucceed(request):
    return render(request, 'register/registerSucceed.html')


def login(request):
    # 已登入直接跳轉
    if request.user.is_authenticated:
        return redirect(reverse_lazy('mutualClubList'))

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        account = request.POST.get('account')
        signature = request.POST.get('signature')
        message = request.POST.get('message')

        if username is not None:
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return redirect(reverse_lazy('loginSucceed'))
            else:
                hasError = True
                context = {
                    'hasError': hasError
                }
                return render(request, 'login/login.html', context)
        else:
            try:
                user = User.objects.get(username=account)
            except User.DoesNotExist:
                user = None
            if user:
                if (checkSignature(signature, message) == account):
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    auth.login(request, user)
                    return redirect(reverse_lazy('loginSucceed'))
                else:
                    context = {
                        "addr": account,
                        "recover": (signature, message),
                    }
                    return render(request, 'login.html', context)
            else:
                User.objects.create(
                    username=account,
                    password=make_password(secrets.token_hex(32)),
                )
                user = User.objects.get(username=account)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                auth.login(request, user)
                return redirect(reverse_lazy('loginSucceed'))
    hasError = False
    context = {'hasError': hasError}
    return render(request, 'login/login.html', context)


def signNonce(request):
    nonce = secrets.token_hex(32)
    return JsonResponse({'nonce': nonce})


def checkSignature(signature, message):
    message_hash = encode_defunct(text=message)
    address = web3.eth.account.recover_message(
        message_hash, signature=signature)
    return address


def loginSucceed(request):
    return render(request, 'login/loginSucceed.html')


def logout(request):
    auth.logout(request)
    return redirect(reverse_lazy('login'))

# Cash Point


@csrf_exempt
def buyCashPoint(request):
    sharedAddress = web3.toChecksumAddress(
        "0xac0868B1DcA15532d7EaCF8fA1eE5bcae0300D1A")
    account = request.user.username
    address = ""
    context = {
        'account': account,
    }
    if request.POST:
        amount = request.POST.get('amount')
        try:
            address = web3.toChecksumAddress('account')
        except:
            address = sharedAddress
        return HttpResponse(cashPointOrder(address, account, amount))
    return render(request, 'payment/buyCashPoint.html', context)

# @method_decorator(csrf_exempt, name='dispatch')


class PaymentReturnView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentReturnView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        context = {}
        res = request.POST.dict()
        recipient = web3.toChecksumAddress(res['CustomField1'])
        username = res['CustomField3']
        amount = int(res['TradeAmt'])
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
        receiptThread = BuyCashPointReceiptThread(txHash, recipient, username)
        receiptThread.start()
        t = loader.get_template('payment/paymentSuccess.html')
        context.update({
            "res": res,
            "tx_hash": txHash
        })
        return HttpResponse(t.render(context, request))


def develop(request):
    return render(request, 'test.html')

def cashOut(request):
    user = request.user
    userInfo = UserInfo.objects.get(user=user)
    sharedAddress = web3.toChecksumAddress( "0xac0868B1DcA15532d7EaCF8fA1eE5bcae0300D1A")
    if userInfo.wallet_address == sharedAddress:
        blockchainUser = False
    else:
        blockchainUser = True
    context = {
        'user': user,
        'userInfo': userInfo,
        'blockchainUser': blockchainUser,
    }
    if request.POST:
        value = request.POST.get('value')
        if blockchainUser:
            signature = request.POST.get('signature')
            sigNonce = request.POST.get('nonce')
            transferERC865(user.username, signature, value, sigNonce)
            return redirect(reverse_lazy('cashOutSucceed'))
        else:
            userInfo.cash_points -= int(value)
            userInfo.save()
            return redirect(reverse_lazy('cashOutSucceed'))
    return render(request, 'payment/cashOut.html', context)

def cashOutSucceed(request):
    user=request.user
    userInfo = UserInfo.objects.get(user=user)
    context ={
        'userInfo':userInfo
    }
    return render(request, 'payment/cashOutSucceed.html',context)

def transferERC865(username, signature, value, sigNonce):

    # --- 轉換成 transferPreSigned() 接受的資料型態 ---
    signature.encode('utf-8')
    value = int(value)
    sigNonce = int(sigNonce)
    wishListID = int(1)
    itemID = int(1)
    quantity = int(1)
    # --- 轉換成 transferPreSigned() 接受的資料型態 ---

    # --- 查詢 nonce、gas 試算 ---
    nonce = web3.eth.getTransactionCount(TTethereum.developerPublicKey)
    # --- 查詢 nonce、gas 試算 ---

    # --- 打包交易、簽章、送出 ---
    txn = TTethereum.cashPointContract.functions.transferPreSigned(signature, TTethereum.developerPublicKey, value, 0, sigNonce, wishListID, itemID, quantity).buildTransaction({
        'chainId': 3,
        'gas': 370000,
        'gasPrice': web3.eth.gas_price,
        'nonce': nonce
    })
    signed_txn = web3.eth.account.signTransaction(txn, private_key=TTethereum.developerPrivateKey)
    txHash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    receiptThread = TransferCashPointReceiptThread(txHash, username)
    receiptThread.start()