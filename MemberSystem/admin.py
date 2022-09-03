from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'birthday', 'ID_number', 'bank_account']

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ['user', 'action_type', 'target', 'amount', 'request_time', 'act_time']