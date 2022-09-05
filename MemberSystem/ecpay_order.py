import importlib.util
from datetime import datetime
from django.conf import settings
import hashlib

spec = importlib.util.spec_from_file_location(
    "ecpay_payment_sdk",
    "MemberSystem/ecpay_payment_sdk.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def cashPointOrder(userAddress, username, amount):
    order_params = {
        # === 付款資訊 ===
        "ReturnURL": "http://127.0.0.1:8000/zh-hant/members/paymentReturn/",   # 開發本機端 
        # "ReturnURL": "http://52.73.1.77:8000/zh-hant/members/paymentReturn/",  # EC2主機端 
        "ChoosePayment": "ALL",
        "PaymentType": "aio",

        # === 訂單資訊 ===
        # 訂單編號，要求(1)唯一(2)20碼，所以將使用者帳號+當前時間做hash並取前20碼。
        "MerchantTradeNo": hashlib.md5(
            (userAddress + str(datetime.now())).encode()).hexdigest()[0:20],
        # 訂單建立日期
        "MerchantTradeDate": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),

        # 商品資訊
        "TotalAmount": amount,
        "TradeDesc": "現金點數儲值",
        "ItemName": "風險互助專案 現金點數",

        # === 選填欄位 ===
        "CustomField3": username,
        "CustomField1": userAddress,
        "CustomField2": "cashPointContract",
        # "OrderResultURL": "http://52.73.1.77:8000/zh-hant/members/paymentReturn/",  # EC2主機端 
        "OrderResultURL": "http://127.0.0.1:8000/zh-hant/members/paymentReturn/",  # 用這個 view 接結果 # 開發本機端 
    }
    # 建立訂單實體
    ecpay_payment_sdk = module.ECPayPaymentSdk(
        MerchantID=settings.ECPAY_MERCHEAT_ID,
        HashKey=settings.ECPAY_API_HASH_KEY,
        HashIV=settings.ECPAY_API_HASH_IV
    )
    try:
        # 產生綠界訂單所需參數
        final_order_params = ecpay_payment_sdk.create_order(order_params)

        # 產生 html 的 form 格式
        action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'  # 測試環境
        # action_url = 'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5' # 正式環境
        html = ecpay_payment_sdk.gen_html_post_form(action_url, final_order_params)

        # 最後產出 html，回傳回去顯示此 html
        return html
    except Exception as error:
        print('An exception happened: ' + str(error))