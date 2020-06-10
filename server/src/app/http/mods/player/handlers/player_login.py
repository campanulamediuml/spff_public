
from app.http.handler_base import HandlerBase
from tornado.concurrent import run_on_executor

from app.http.relay.relay import Relay
from sdk.sdk_api import sdk_api
from data.server import Data
from error import error


class player_login(HandlerBase):
    @run_on_executor
    def post(self):
        data = self.get_post_data()
        login_type=[]

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
        token = self.login(user_id,character='player')
        # 用户存在则做登录操作
        reply = {
            'token': token,
        }
        self.send_ok(reply)
        return

    def check_user(self,player_base):
        player_info = Data.find('player',[('open_id','=',player_base['open_id'])])
        if player_info != None:
            Data.update('player',[('id','=',player_info['id'])],player_base)
        else:
            Data.insert('player',player_base)

        player_info = Data.find('player',[('open_id','=',player_base['open_id'])])
        return player_info['id']
    # 针对用户信息的更新和添加


class player_logout(HandlerBase):
    @run_on_executor()
    def get(self):
        admin_base = self.get_user_base(Relay.player)
        if admin_base == None:
            self.send_faild(error.ERROR_PLAYER_NO_LOGIN)
            return
        self.logout('player')
        # res = {}
        if self.get_user_base(Relay.player) != None:
            self.send_faild(error.ERROR_FAIL)
        else:
            self.send_ok({})
        return
    # 退出登录