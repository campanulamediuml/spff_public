from tornado.concurrent import run_on_executor

from app.http.handler_base import HandlerBase
from data.server import Data
from common.common import common_tools as common
import time

from error import error


class change_pw(HandlerBase):
    @run_on_executor
    def post(self):
        data = self.get_post_data()
        # character = data['character']
        character='admin'
        user_base = self.get_user_base(character)
        if user_base == None:
            self.send_faild(error.ERROR_ADMIN_NO_LOGIN)
            return

        if data['pw_1'] != data['pw_2']:
            self.send_faild(error.ERROR_PW_DIFF)
            return

        if common.get_md5(data['pw_old']) != user_base['pwhash']:
            self.send_faild(error.ERROR_PW_ERROR)
            return

        params = {
            'pwhash':common.get_md5(data['pw_1'])
        }
        Data.update(character,[('id','=',user_base['id'])],params)
        self.send_ok({})
        return