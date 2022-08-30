from django.shortcuts import render
from django.http import HttpResponse

from datetime import datetime
from .models import *

# Create your views here.

def landingPage(request):
    return render(request,'landingPage/landingPage.html')

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
            print(joinFee, launchAmount, terminateNums, deadline, deadlineDate, paymentContentOption)
        else:
            print(joinFee, launchAmount, terminateNums, deadline, paymentContentOption)
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
            print(joinFee, launchAmount, terminateNums, terminateAmount, deadline, deadlineDate, paymentContentOption)
        else:
            print(joinFee, launchAmount, terminateNums, terminateAmount, deadline, paymentContentOption)
    return render(request, 'startPlan/createShareClub.html')

def sharingClubList(request):
    return render(request, 'joinPlan/sharingClubList.html')

def mutualClubList(request):
    planList = Plan.objects.all()
    context = {
        'planList' : planList,
    }
    return render(request, 'joinPlan/mutualClubList.html', context)

def joinMutualClubVerify(request, id):
    plan = Plan.objects.get(id=id)
    context = {
        'plan' : plan,
    }
    return render(request, 'joinPlan/joinMutualVerify.html', context)

def joinMutualClubStep2(request, id):
    plan = Plan.objects.get(id=id)
    context = {
        'plan' : plan,
    }
    return render(request, 'joinPlan/joinMutualStep2.html', context)

def createMutualClub(request):
    return render(request, 'createMutualClub.html')