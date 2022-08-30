from django.urls import path

from Club.views import *
from Club.forms import *


urlpatterns = [
    path('startPlan/verify', verify, name='verify'),
    path('startPlan/riskPool', riskPool, name='riskPool'),
    path('startPlan/individualPlan', createIndividualPlan, name='individualPlan'),
    path('startPlan/createShareClub', createShareClub, name='createShareClub'),
    path('startPlan/createMutualHelpClub', createMutualHelpClub, name='createMutualHelpClub'),

    path('sharingClubs', sharingClubList, name='sharingClubList'),
    path('mutualClubs', mutualClubList, name='mutualClubList'),
    path('mutualClubs/create', createMutualClub, name='createMutualClub'),
    path('mutualClubs/<int:id>/verify', joinMutualClubVerify, name='joinMutualClubVerify'),
    path('mutualClubs/<int:id>/step_02', joinMutualClubStep2, name='joinMutualClubStep2')

]