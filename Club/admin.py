from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['contract_address', 'plan_type', 'plan_host', 'fee', 'launch_amount', 'unlimited_period', 'deadline', 'minimum_amounts', 'minimum_participants', 'benefits']

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['plan', 'wallet_address', 'tokens', 'role', 'join_date', 'take_effect_date', 'quit_date']