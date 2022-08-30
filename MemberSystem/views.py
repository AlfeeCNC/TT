import secrets
import json

from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm

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


def register(request):
    # 已登入直接跳轉
    # if request.user.is_authenticated():
    #     return redirect(reverse_lazy('mutualClubs'))

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
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
                    'hasError':hasError
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
    context = {'hasError':hasError}
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
