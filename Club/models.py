from django.db import models
from django.conf import settings

from MemberSystem.models import *


# Create your models here.
class Plan(models.Model):
    name = models.CharField(max_length=20)
    # 計畫TT合約地址
    contract_address = models.CharField(max_length=50)
    # 計畫類型（eg.團體分擔）
    plan_type = models.CharField(max_length=20)
    # 計畫發起人
    plan_host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='plans',
        on_delete=models.CASCADE)
    # 參與費用
    fee = models.PositiveIntegerField()
    # 起始金額
    launch_amount = models.PositiveIntegerField()
    # 是否為無限期
    unlimited_period = models.BooleanField()
    # 終止時間
    deadline = models.DateField(null=True, blank=True) # 因可為無限期所以可為空
    # 群募終止金額
    minimum_amounts = models.PositiveIntegerField()
    # 群募終止人數
    minimum_participants = models.PositiveIntegerField()
    # 給付內容
    benefits = models.CharField(max_length=20)

    def __str__(self):
        return self.contract_address

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
        on_delete=models.CASCADE,
        null=True) # 可能為非區塊鏈使用者，可設空值
    # 持有板機憑證數量
    tokens = models.IntegerField()
    # 參與者的角色（eg.資金提供人）
    role = models.CharField(max_length=20)
    # 參與者加入日期
    join_date = models.DateField()
    # 生效日期
    take_effect_date = models.DateField()
    # 退出日期
    quit_date = models.DateTimeField()

    def __str__(self):
        return self.id