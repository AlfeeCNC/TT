from django.urls import path

from .views import *

urlpatterns = [
    # login/logout
    path('', adminLogin, name='adminLogin'),
    path('dashboard', adminDashboard, name='adminDashboard'),

    path('token/issue/<slug:target>', tokenIssue, name='tokenIssue'),
] 