
from app.http.handler_base import HandlerBase
from tornado.concurrent import run_on_executor

from app.http.mods.admin.admin_tools import admin_tool
from app.http.relay.relay import Relay
from sdk.sdk_api import sdk_api
from data.server import Data
from error import error


class player_login(HandlerBase):
    login_type_wechat = 1
    login_type_pw = 2

    @run_on_executor
    def post(self):
        data = self.get_post_data()
        login_type_dict = {
            player_login.login_type_wechat:self.login_by_wechat,
            player_login.login_type_pw: self.login_by_pw
        }

        login_type = data['login_type']
        if login_type not in login_type_dict:
            self.send_faild(error.ERROR_FAIL)
            return
        method = login_type_dict[login_type]
        method(data)
        return


    def login_by_pw(self,data):
        username = data['username']
        pw = data['pswd']

        user = Data.find(Relay.player, [('username', '=', username)])
        if user == None:
            self.send_faild(error.ERROR_NO_ADMIN)
            return

        if admin_tool.check_pw(user, pw) is False:
            self.send_faild(error.ERROR_PW_ERROR)
            return

        token = self.login(user['id'], character=Relay.player)
        res = {
            'token': token
        }
        self.send_ok(res)
        return



    def check_user(self,player_base):
        player_info = Data.find(Relay.player,[('open_id','=',player_base['open_id'])])
        if player_info != None:
            Data.update(Relay.player,[('id','=',player_info['id'])],player_base)
        else:
            Data.insert(Relay.player,player_base)

        player_info = Data.find(Relay.player,[('open_id','=',player_base['open_id'])])
        return player_info['id']
    # 针对用户信息的更新和添加

    def login_by_wechat(self,data):
        try:
            wechat_verify_code = data['code']
        except Exception as e:
            print(str(e))
            return self.send_faild(error.ERROR_PARAM)

        player_base = sdk_api.wechat_login(wechat_verify_code)
        if player_base is None:
            return self.send_faild(error.ERROR_NO_PLAYER)

        user_id = self.check_user(player_base)
        # 确认用户是否存在，如果不存在就写入数据库
        token = self.login(user_id,character=Relay.player)
        # 用户存在则做登录操作
        reply = {
            'token': token,
        }
        self.send_ok(reply)
        return



class player_logout(HandlerBase):
    @run_on_executor()
    def get(self):
        admin_base = self.get_user_base(Relay.player)
        if admin_base == None:
            self.send_faild(error.ERROR_PLAYER_NO_LOGIN)
            return
        self.logout(Relay.player)
        # res = {}
        if self.get_user_base(Relay.player) != None:
            self.send_faild(error.ERROR_FAIL)
        else:
            self.send_ok({})
        return
    # 退出登录