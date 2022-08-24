from django.db import models
from django.conf import settings

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
    birthday = models.DateField
    # 使用者身分證字號
    ID_number = models.CharField(max_length=20)
    # 使用者銀行帳戶
    bank_account = models.CharField(max_length=30)

    def __str__(self):
        return self.ID_number

class Wallet(models.Model):
    # 使用者
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_wallet',
        on_delete=models.CASCADE)
    # 使用者錢包地址
    wallet_address = models.CharField(max_length=50)
    # 使用者現金點數
    cash_points = models.PositiveIntegerField()
    # 使用者是否為白名單
    is_whitelist = models.BooleanField(default=True)

    def __str__(self):
        return self.wallet_address