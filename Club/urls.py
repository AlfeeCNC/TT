from django.urls import path

from .views import *
from .forms import *


urlpatterns = [
    path('detail/<slug:address>', clubDetail, name='clubDetail'),

    path('startPlan/verify', verify, name='verify'),
    path('startPlan/riskPool', riskPool, name='riskPool'),
    path('startPlan/individualPlan', createIndividualPlan, name='individualPlan'),
    path('startPlan/createShareClub', createShareClub, name='createShareClub'),
    path('startPlan/createMutualHelpClub', createMutualHelpClub, name='createMutualHelpClub'),

    path('sharingClubs', sharingClubList, name='sharingClubList'),
    path('mutualClubs', mutualClubList, name='mutualClubList'),
    path('mutualClubs/<slug:address>/verify', joinMutualClubVerify, name='joinMutualClubVerify'),
    path('mutualClubs/<slug:address>/step_02', joinMutualClubStep2, name='joinMutualClubStep2'),
    path('mutualClubs/<slug:address>/joinSucceed', joinClubSucceed, name='joinClubSucceed'),

    path('<path:address>/quit', quitClub, name='quitClub' ),
    path('<path:address>/quit/succeed', quitClubSucceed, name='quitClubSucceed' ),


    path('<path:address>/decrease', decrease, name='decrease' ),
    path('<path:address>/decrease/<path:action>/succeed', decreaseSucceed, name='decreaseSucceed' ),

    path('<path:address>/applyForClaim', applyForClaim, name='applyForClaim' ),
    path('<path:address>/applyForClaimSucceed/<path:action>/succeed', applyForClaimSucceed, name='applyForClaimSucceed' ),

    path('serviceNotAvailable', serviceNotAvailable, name='serviceNotAvailable'),

]