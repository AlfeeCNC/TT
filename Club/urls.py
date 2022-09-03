from django.urls import path

from .views import *
from .forms import *


urlpatterns = [
    path('startPlan/verify', verify, name='verify'),
    path('startPlan/riskPool', riskPool, name='riskPool'),
    path('startPlan/individualPlan', createIndividualPlan, name='individualPlan'),
    path('startPlan/createShareClub', createShareClub, name='createShareClub'),
    path('startPlan/createMutualHelpClub', createMutualHelpClub, name='createMutualHelpClub'),

    path('sharingClubs', sharingClubList, name='sharingClubList'),
    path('mutualClubs', mutualClubList, name='mutualClubList'),
    path('mutualClubs/create', createMutualClub, name='createMutualClub'),
    path('mutualClubs/<slug:address>/verify', joinMutualClubVerify, name='joinMutualClubVerify'),
    path('mutualClubs/<slug:address>/step_02', joinMutualClubStep2, name='joinMutualClubStep2')

]