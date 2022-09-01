from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'birthday', 'ID_number', 'bank_account']

# @admin.register(Wallet)
# class WalletAdmin(admin.ModelAdmin):
#     list_display = ['user', 'wallet_address', 'cash_points', 'is_whitelist']