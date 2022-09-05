from django.db import models
from django.conf import settings
from django.urls import reverse

from Club.models import *

# Create your models here.
class UserInfo(models.Model):
    # 外鍵，使用者
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_info',
        on_delete=models.CASCADE)
    # 使用者姓名
    name = models.CharField(max_length=20)
    # 使用者出生年月日
    birthday = models.DateField()
    # 使用者身分證字號
    ID_number = models.CharField(max_length=20)
    # 使用者銀行帳戶
    bank_account = models.CharField(max_length=30)
    # 使用者錢包地址
    wallet_address = models.CharField(max_length=50, null=True, blank=True)
    # 使用者現金點數
    cash_points = models.PositiveIntegerField(null=True, blank=True,)
    # 是否是白名單
    is_whitelist = models.BooleanField(default=False)

    def __str__(self):
        return self.ID_number

class Action(models.Model):
    # 使用者
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_action',
        on_delete=models.CASCADE)
    # 動作類別，e.g. 出金、入金、加入群組...等
    action_type = models.CharField(max_length=20)
    # 動作的目標，e.g.加入哪個群組
    target = models.ForeignKey(
        Plan,
        related_name='target_plan',
        on_delete=models.CASCADE)
    # 數量，e.g.投保的憑證數量（第一階段先亂定數目，因為這關係到核保步驟）
    amount = models.IntegerField(null=True, blank=True)
    # 提出請求的時間
    request_time = models.DateTimeField()
    # 實際執行的時間
    act_time = models.DateTimeField()
    # 是否已執行
    done = models.BooleanField(default=False)
    # transaction hash
    tx_hash = models.CharField(max_length=100, null=True, blank=True)