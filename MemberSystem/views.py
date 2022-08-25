import secrets
import json

from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

import web3
from web3 import Web3
from eth_account.messages import encode_defunct

# Infura Node
InfuraURL = "https://ropsten.infura.io/v3/ed00ddb25c3b460c9b99f2375a314102"
# Initiating Web3
web3 = Web3(web3.HTTPProvider(InfuraURL))

# Create your views here.
def myPortfolio(request):
    return render(request, 'userDashboard/portfolio.html')

# Single-Sign-On via MetaMask
def login(request):
    if request.POST:
        account = request.POST.get('account')
        signature = request.POST.get('signature')
        message = request.POST.get('message')
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
    return render(request, 'login/login.html')

def signNonce(request):
    nonce = secrets.token_hex(32)
    return JsonResponse({'nonce': nonce})

def checkSignature(signature, message):
    message_hash = encode_defunct(text=message)
    address = web3.eth.account.recover_message(message_hash, signature=signature)
    return address

def loginSucceed(request):
    if request.POST:
        return redirect(reverse_lazy('verify'))
    return render(request, 'login/loginSucceed.html')


def logout(request):
    auth.logout(request)
    return redirect(reverse_lazy('login'))