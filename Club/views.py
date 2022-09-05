import datetime
import re
from this import d
import requests
import json

from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Q
from .models import *
from MemberSystem.models import *

import web3
from web3 import Web3
from eth_account.messages import encode_defunct

from MemberSystem.models import *

# Infura Node
InfuraURL = "https://ropsten.infura.io/v3/ed00ddb25c3b460c9b99f2375a314102"
# Initiating Web3
web3 = Web3(web3.HTTPProvider(InfuraURL))

# Create your views here.


def landingPage(request):
    return render(request, 'landingPage/landingPage.html')


def verify(request):
    return render(request, 'startPlan/verify.html')


def riskPool(request):
    return render(request, 'startPlan/chooseRiskPool.html')


def createIndividualPlan(request):
    if request.POST:
        joinFee = request.POST['joinFee']
        launchAmount = request.POST['launchAmount']
        deadline = request.POST['deadline']
        paymentContentOption = request.POST['paymentContentOption']
        print(joinFee, launchAmount, deadline, paymentContentOption)
    return render(request, 'startPlan/individualPlan.html')


def createMutualHelpClub(request):
    if request.POST:
        joinFee = request.POST['joinFee']
        launchAmount = request.POST['launchAmount']
        terminateNums = request.POST['terminateNums']
        deadline = request.POST['deadline']
        paymentContentOption = request.POST['paymentContentOption']
        if deadline == "有期限":
            deadlineDate = request.POST['deadlineDate']
            print(joinFee, launchAmount, terminateNums,
                  deadline, deadlineDate, paymentContentOption)
        else:
            print(joinFee, launchAmount, terminateNums,
                  deadline, paymentContentOption)
    return render(request, 'startPlan/createMutualHelpClub.html')


def createShareClub(request):
    if request.POST:
        joinFee = request.POST['joinFee']
        launchAmount = request.POST['launchAmount']
        terminateNums = request.POST['terminateNums']
        terminateAmount = request.POST['terminateAmount']
        deadline = request.POST['deadline']
        paymentContentOption = request.POST['paymentContentOption']
        if deadline == "有期限":
            deadlineDate = request.POST['deadlineDate']
            print(joinFee, launchAmount, terminateNums, terminateAmount,
                  deadline, deadlineDate, paymentContentOption)
        else:
            print(joinFee, launchAmount, terminateNums,
                  terminateAmount, deadline, paymentContentOption)
    return render(request, 'startPlan/createShareClub.html')


def sharingClubList(request):
    return render(request, 'joinPlan/sharingClubList.html')


def mutualClubList(request):
    planList = Plan.objects.all()
    for plan in planList:
        requestURL = "https://ttdapplet.skychainnet.com/api/supply"
        requestData = {
            "domain": "skychainnet.com",
            "domain_password": "skychain",
            "tt_address": plan.contract_address
        }
        tokenSupplyAPI = requests.post(requestURL, json=requestData)
        response = json.loads(tokenSupplyAPI.content)
        supply = int(response['supply'])//1000000000000000000
        plan.supply = supply
    context = {
        'planList': planList,
    }
    return render(request, 'joinPlan/mutualClubList.html', context)


def joinMutualClubVerify(request, address):
    plan = Plan.objects.get(contract_address=address)
    context = {
        'plan': plan,
    }
    return render(request, 'joinPlan/joinMutualVerify.html', context)


@csrf_exempt
def joinMutualClubStep2(request, address):
    plan = Plan.objects.get(contract_address=address)
    user = request.user
    try:
        if user.username == web3.toChecksumAddress(user.username):
            userType = "區塊鏈使用者"
            address = user.username
    except:
        userType = "非區塊鏈使用者（使用公共錢包）"
        address = "0xac0868B1DcA15532d7EaCF8fA1eE5bcae0300D1A"
    context = {
        'plan': plan,
        'userType': userType,
        'address': address,
    }
    if request.POST:
        user = request.user
        action_type = "join"
        target = plan
        amount = 13
        request_time = datetime.datetime.now()
        act_time = datetime.datetime(
            request_time.year, request_time.month+1, 1)
        action = Action(user=user, action_type=action_type,
                        target=target, amount=amount, request_time=request_time,
                        act_time=act_time, done=False)
        action.save()
        return redirect('joinClubSucceed', address=plan.contract_address)
    return render(request, 'joinPlan/joinMutualStep2.html', context)


def joinClubSucceed(request, address):
    plan = Plan.objects.get(contract_address=address)
    context = {
        "plan": plan,
    }
    return render(request, 'joinPlan/joinClubSucceed.html', context)


def clubDetail(request, address):
    plan = Plan.objects.get(contract_address=address)
    address = web3.toChecksumAddress(address)
    claims = Action.objects.filter(Q(action_type='claim')|Q(action_type='claimThenBurn'), done=True, target=plan)
    claimAmount = 0
    try:
        for claim in claims:
            claimAmount += claim.amount
    except:
        claimAmount = 0
    requestURL = "https://ttdapplet.skychainnet.com/api/supply"
    requestData = {
        "domain": "skychainnet.com",
        "domain_password": "skychain",
        "tt_address": address
    }
    tokenSupplyAPI = requests.post(requestURL, json=requestData)
    response = json.loads(tokenSupplyAPI.content)
    supply = int(response['supply'])//1000000000000000000
    payments = Action.objects.filter(target=plan, action_type="payment")
    context = {
        'claims' : claims,
        'claimAmount' : claimAmount,
        'plan': plan,
        'supply': supply,
        'payments': payments,
    }
    return render(request, 'clubDetail.html', context)


def quitClub(request, address):
    user = request.user
    plan = Plan.objects.get(contract_address=address)
    participanting = Participant.objects.get(user=user, plan=plan)
    amount = participanting.tokens
    requestTime = datetime.datetime.now()
    context = {
        'participanting': participanting
    }
    if request.POST:
        Action.objects.create(
            user=user,
            action_type="quit",
            target=plan,
            amount=amount,
            request_time=requestTime,
            act_time=datetime.datetime(
                requestTime.year, requestTime.month+1, 1),
            done=False
        )
        participanting.quitting = True
        participanting.save()
        return redirect(reverse_lazy('quitClubSucceed', kwargs={'address': address}))
    return render(request, 'quitClub.html', context)


def quitClubSucceed(request, address):
    user = request.user
    plan = Plan.objects.get(contract_address=address)
    participanting = Participant.objects.get(user=user, plan=plan)
    context = {
        'participanting': participanting
    }
    return render(request, 'quitClubSucceed.html', context)


def decrease(request, address):
    user = request.user
    plan = Plan.objects.get(contract_address=address)
    participanting = Participant.objects.get(user=user, plan=plan)
    amount = request.POST.get('amount')
    requestTime = datetime.datetime.now()
    context = {
        'participanting': participanting
    }
    if request.POST:
        action = Action(
            user=user,
            action_type="decrease",
            target=plan,
            amount=amount,
            request_time=requestTime,
            act_time=datetime.datetime(
                requestTime.year, requestTime.month+1, 1),
            done=False
        )
        action.save()
        return redirect(reverse_lazy('decreaseSucceed', kwargs={'address': address, 'action':action.id }))
    return render(request, 'decrease.html', context)


def decreaseSucceed(request, address, action):
    user = request.user
    action = Action.objects.get(id=action)
    plan = Plan.objects.get(contract_address=address)
    participanting = Participant.objects.get(user=user, plan=plan)
    context = {
        'participanting': participanting,
        'action':action
    }
    return render(request, 'decreaseSucceed.html', context)

def applyForClaim(request, address):
    user = request.user
    plan = Plan.objects.get(contract_address=address)
    participanting = Participant.objects.get(user=user, plan=plan)
    amount = participanting.tokens
    requestTime = datetime.datetime.now()
    context = {
        'participanting': participanting
    }
    if request.POST:
        claimType = request.POST.get('claimType')
        action = Action(
            user=user,
            action_type=claimType,
            target=plan,
            amount=amount,
            request_time=requestTime,
            act_time=datetime.datetime(
                requestTime.year, requestTime.month+1, 1),
            done=False
        )
        action.save()
        return redirect(reverse_lazy('applyForClaimSucceed', kwargs={'address': address, 'action':action.id }))
    return render(request, 'claim.html', context)


def applyForClaimSucceed(request, address, action):
    user = request.user
    action = Action.objects.get(id=action)
    plan = Plan.objects.get(contract_address=address)
    participanting = Participant.objects.get(user=user, plan=plan)
    context = {
        'participanting': participanting,
        'action':action
    }
    return render(request, 'claimSucceed.html', context)

def serviceNotAvailable(request):
    return render(request, 'serviceNotAvailable.html')
