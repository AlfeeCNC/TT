from django.urls import path

from .views import *

urlpatterns = [
    # login/logout
    path('', adminLogin, name='adminLogin'),
    path('dashboard', adminDashboard, name='adminDashboard'),
    path('setWhitelist', setWhitelist, name='setWhitelist'),

    path('claim/<path:target>/<path:user>/<path:taskID>', claim, name='makeClaim'),


    path('token/issue/<path:target>', tokenIssue, name='tokenIssue'),
    path('token/burn/<path:target>/<path:user>/<path:taskID>', tokenBurn, name='tokenBurn'),
] 