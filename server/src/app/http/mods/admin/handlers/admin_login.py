from app.http.handler_base import HandlerBase
from tornado.concurrent import run_on_executor
from app.http.mods.admin.admin_tools import admin_tool
from app.http.relay.relay import Relay
from data.server import Data
from error import error

class admin_login(HandlerBase):
    @run_on_executor
    def post(self):
        data = self.get_post_data()
        username = data['username']
        pw = data['pswd']

        user = Data.find(Relay.admin,[('username','=',username)])
        if user == None:
            self.send_faild(error.ERROR_NO_ADMIN)
            return

        if admin_tool.check_pw(user,pw) is False:
            self.send_faild(error.ERROR_PW_ERROR)
            return

        token = self.login(user['id'],character=Relay.admin)
        res = {
            'token':token
        }
        self.send_ok(res)
        return
        # 登录


class admin_logout(HandlerBase):
    @run_on_executor
    def post(self):
        admin_base = self.get_user_base(Relay.admin)
        if admin_base == None:
            self.send_faild(error.ERROR_ADMIN_NO_LOGIN)
            return
        self.logout('admin')
        # res = {}
        if self.get_user_base(Relay.admin) != None:
            self.send_faild(error.ERROR_FAIL)
        else:
            self.send_ok({})
        return
    # 退出登录

