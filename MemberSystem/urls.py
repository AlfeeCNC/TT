from django.urls import path

from MemberSystem.views import *


urlpatterns = [
    path('myPortfolio', myPortfolio, name='myPortfolio'),
]