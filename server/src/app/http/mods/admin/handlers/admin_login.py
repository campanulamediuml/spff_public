from werkzeug.security import check_password_hash

from app.http.handler_base import HandlerBase
from tornado.concurrent import run_on_executor

from app.http.relay.relay import Relay
from common.common import common_tools
from data.server import Data
from error import error

class admin_login(HandlerBase):
    @run_on_executor
    def post(self):
        data = self.get_post_data()
        username = data['username']
        pw = data['pswd']

        user = Data.find('admin',[('username','=',username)])
        if user == None:
            self.send_faild(error.ERROR_NO_ADMIN)
            return
        if common_tools.get_md5(pw) != user['pwhash']:
            self.send_faild(error.ERROR_NO_ADMIN)
            return

        token = self.login(user['id'],character='admin')
        res = {
            'token':token
        }
        self.send_ok(res)
        return
        # 登录


class admin_logout(HandlerBase):
    @run_on_executor
    def post(self):
        admin_base = self.get_user_base('admin')
        if admin_base == None:
            self.send_faild(error.ERROR_ADMIN_NO_LOGIN)
            return
        self.logout('admin')
        # res = {}
        if self.get_user_base('admin') != None:
            self.send_faild(error.ERROR_FAIL)
        else:
            self.send_ok({})
        return
    # 退出登录

