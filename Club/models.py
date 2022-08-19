from django.db import models
from django.contrib.auth.models import User

from MemberSystem.models import *


# Create your models here.
class Plan(models.Model):
    # 計畫類型（eg.團體分擔）
    plan_type = models.CharField(max_length=20)
    # 計畫發起人
    plan_host = models.ForeignKey(
        User,
        related_name='plans',
        on_delete=models.CASCADE)
    # 參與費用
    join_fee = models.PositiveIntegerField()
    # 起始金額
    launch_amount = models.PositiveIntegerField()
    # 是否為無限期
    indefinitely = models.BooleanField()
    # 終止時間
    deadline = models.DateField()
    # 群募終止金額
    terminate_amount = models.PositiveIntegerField()
    # 群募終止人數
    terminate_nums = models.PositiveIntegerField()
    # 支付內容
    payment_content = models.CharField(max_length=20)

class Participant(models.Model):
    # 參與者參加的計畫
    plan = models.ForeignKey(
        Plan,
        related_name='participant',
        on_delete=models.CASCADE)
    # 參與者的錢包地址
    wallet_address = models.ForeignKey(
        Wallet,
        related_name='participant_wallet',
        on_delete=models.CASCADE)
    # 參與者的角色（eg.資金提供人）
    role = models.CharField(max_length=20)
    # 參與者加入日期
    join_date = models.DateField()
    # 生效日期
    take_effect_date = models.DateField()
    # 退出日期
    quit_date = models.DateTimeField()