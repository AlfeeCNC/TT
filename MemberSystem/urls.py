from django.urls import path

from .views import *


urlpatterns = [
    # register
    path('register', register, name='register'),
    path('usernameExisted', usernameExisted, name='usernameExisted'),
    path('register/succeed', registerSucceed, name='registerSucceed'),
    
    # login/logout
    path('login', login, name='login'),
    path('login/succeed', loginSucceed, name='loginSucceed'),
    path('logout', logout, name='logout'),

    # Portfolio
    path('myPortfolio', myPortfolio, name='myPortfolio'),

    # buy cash point
    path('buyCashPoint/', buyCashPoint, name='buyCashPoint'),
    path('paymentReturn/', PaymentReturnView.as_view(), name='paymentReturn'),
    path('develop', develop, name='develop'),

    # cash out
    path('cashOut', cashOut, name='cashOut'),
    path('cashOut/succeed', cashOutSucceed, name='cashOutSucceed'),
]