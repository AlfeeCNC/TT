import re
from django.shortcuts import render
from django.http import HttpResponse

from datetime import datetime
from .forms import FormStepOne, FormStepTwo
from formtools.wizard.views import SessionWizardView


# Create your views here.

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
    return render(request, 'startPlan/createMutualHelpClub.html')

def createShareClub(request):
    return render(request, 'startPlan/createShareClub.html')

class FormWizardView(SessionWizardView):
    form_list = [FormStepOne, FormStepTwo]

    def get_template_names(self):
        return ['startPlanForm/step{0}.html'.format(self.steps.current)]
    
    def done(self, form_list, **kwargs):
        return render(self.request, 'done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })