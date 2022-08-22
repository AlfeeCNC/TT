from urllib import request
from django.shortcuts import render

# Create your views here.
def myPortfolio(request):
    return render(request, 'userDashboard/portfolio.html')