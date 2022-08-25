from django.urls import path

from MemberSystem.views import *


urlpatterns = [
    path('login', login, name='login'),
    path('login/succeed', loginSucceed, name='loginSucceed'),
    path('logout', logout, name='logout'),
    path('myPortfolio', myPortfolio, name='myPortfolio'),
]