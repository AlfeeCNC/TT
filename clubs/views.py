import re
from django.shortcuts import render
from django.http import HttpResponse

from datetime import datetime
from .forms import FormStepOne, FormStepTwo
from formtools.wizard.views import SessionWizardView


# Create your views here.

def verify(request):
    return render(request, 'startPlanForm/verify.html')

def riskPool(request):
    return render(request, 'startPlanForm/chooseRiskPool.html')

def createIndividualPlan(request):
    return render(request, 'startPlanForm/individualPlan.html')

class FormWizardView(SessionWizardView):
    form_list = [FormStepOne, FormStepTwo]

    def get_template_names(self):
        return ['startPlanForm/step{0}.html'.format(self.steps.current)]
    
    def done(self, form_list, **kwargs):
        return render(self.request, 'done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })