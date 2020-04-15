from sdk.wechat_sdk.wechat_eco import wechat_eco_api
from sdk.wechat_sdk.wechat_auth import wechat_auth_api

class sdk_api(object):
    @staticmethod
    def wechat_pay(remote_ip, openid, gooddesc, money, out_trade_no, buyer):
        return wechat_eco_api.wechat_pay(remote_ip, openid, gooddesc, money, out_trade_no, buyer)

    @staticmethod
    def wechat_pay_to_card(amount,account_number,bank_code,real_name):
        return wechat_eco_api.pay_to_card(amount,account_number,bank_code,real_name)

    @staticmethod
    def wechat_jsapi_ticket(url):
        return wechat_auth_api.get_wechat_jsapi_ticket(url)

    @staticmethod
    def wechat_login(wechat_verify_code):
        return wechat_auth_api.wechat_login(wechat_verify_code)


