from tornado.concurrent import run_on_executor

from app.http.handler_base import HandlerBase
from app.http.mods.admin.admin_tools import admin_tool
from app.http.relay.relay import Relay
from data.server import Data
from error import error


class sign_in(HandlerBase):
    @run_on_executor
    def post(self):
        data = self.get_post_data()
        user_name = data['username']
        pw_1 = data['pw_1']
        pw_2 = data['pw_2']

        if pw_1 != pw_2:
            return self.send_faild(error.ERROR_PW_DIFF)

        if self.check_if_username_exist(user_name) is True:
            return self.send_faild(error.ERROR_USERNAME_EXIST)

        params = {
            'username':user_name,
            'pwhash':admin_tool.create_pw(pw_1)
        }
        Data.insert(Relay.admin,params)
        return self.send_ok({})


    def check_if_username_exist(self, user_name):
        if Data.find(Relay.admin,[('username','=',user_name)]) is not None:
            return True
        return False