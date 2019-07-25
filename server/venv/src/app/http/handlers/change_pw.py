from app.http.handler_base import HandlerBase
from app.data.server import Data
from app.common import common
import time

class change_pw(HandlerBase):
    def get(self):
        user_base = self.get_user_base()
        if user_base == None:
            self.send_faild('TOKEN_ERROR')
            return

        data = self.get_data()

        if data['pw1'] != data['pw2']:
            self.send_faild('PW_NOT_SAME')
            return

        if common.get_md5(data['pw_old']) != user_base['passwd']:
            self.send_faild('LOGIN_PSW_ERROR')
            return

        params = {
            'passwd':common.get_md5(data['pw2'])
        }
        Data.update('user',[('id','=',user_base['id'])],params)
        self.send_ok({})
        return

