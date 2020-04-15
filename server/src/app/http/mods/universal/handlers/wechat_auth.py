from sdk.sdk_api import sdk_api
from config.wechat_config import WST
from app.http.handler_base import HandlerBase
from tornado.concurrent import run_on_executor


class get_appid(HandlerBase):
    @run_on_executor
    def get(self):
        reply = {
            'app_id': WST.APP_ID
        }
        self.send_ok(reply)
        return
    # 获取appid

class get_wechat_cfg(HandlerBase):
    @run_on_executor
    def post(self):
        data = self.get_post_data()
        url = data['url']
        signDct = sdk_api.wechat_jsapi_ticket(url)
        result = {
            'debug': 0,
            'appId': WST.APP_ID,
            'timestamp': signDct['timestamp'],
            'nonceStr': signDct['nonceStr'],
            'signature': signDct['signature'],
        }
        reply = {
            'ticket_data': result
        }
        self.send_ok(reply)
        return
    # 获取微信票据
