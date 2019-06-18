from app.http.handler_base import HandlerBase
from app.data.server import Data
from app.common import common
import time

class login_handler(HandlerBase):
    def get(self):
        data = self.get_data()
        pw_md5 = common.get_md5(data['pw'])
        condition = [
            ('user_name','=',data['username']),
            ('passwd','=',pw_md5)
        ]

        res = Data.find('user',condition)
        if res == None:
            self.send_faild('LOGIN_PSW_ERROR')
            return
        else:
            token = self.get_token(res)
            result = {
                'token':token
            }
            Data.update('user',condition,result)

            self.send_ok(result)
            return


