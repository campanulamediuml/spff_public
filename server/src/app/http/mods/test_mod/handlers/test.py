import json

from app.http.handler_base import HandlerBase
# from app.ws.relay.ws_relay import Relay
from app.http.relay.relay import Relay


class test(HandlerBase):
    def get(self):
        self.send_ok({})
        return

class refresh_login_info(HandlerBase):
    def get(self):
        return

class onlineadmin(HandlerBase):
    def get(self):
        res  = Relay.get_token_dict('admin')
        print(res)
        self.send_ok(res)
        return
