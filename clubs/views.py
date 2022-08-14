from django.shortcuts import render
from django.http import HttpResponse

from datetime import datetime
# Create your views here.



def hello_world(request):
    return render(request, 'hello.html', {
        'current_time': str(datetime.now()),
    })