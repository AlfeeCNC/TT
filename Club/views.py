from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import datetime
from .models import *
from MemberSystem.models import *

import web3
from web3 import Web3
from eth_account.messages import encode_defunct

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
        target = plan.contract_address
        amount = 13
        request_time = datetime.datetime.now()
        act_time = datetime.datetime(
            request_time.year, request_time.month+1, 1)
        action = Action(user=user, action_type=action_type,
                        target=target, amount=amount, request_time= request_time,
                        act_time=act_time, done=False)
        action.save()
    return render(request, 'joinPlan/joinMutualStep2.html', context)


def createMutualClub(request):
    return render(request, 'createMutualClub.html')
