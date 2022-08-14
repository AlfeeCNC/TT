from django.urls import path
from clubs.views import *

urlpatterns = [
    path('hello/', hello_world),
]