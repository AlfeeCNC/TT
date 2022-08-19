from django.urls import path

from Club.views import *
from Club.forms import *


urlpatterns = [
    path('startPlan/verify', verify, name='verify'),
    path('startPlan/riskPool', riskPool, name='riskPool'),
    path('startPlan/individualPlan', createIndividualPlan, name='individualPlan'),
    path('startPlan/createShareClub', createShareClub, name='createShareClub'),
    path('startPlan/createMutualHelpClub', createMutualHelpClub, name='createMutualHelpClub'),
    path('startPlan/forms', FormWizardView.as_view([FormStepOne, FormStepTwo]), name="startPlanForm")
]