from app.http.handler_base import HandlerBase
from app.data.server import Data
from app.common import common
import time
import json

# 隐藏某一条记录，需要管理员身份才能操作

class block_info(HandlerBase):
    def get(self):
        data = self.get_data()
        user_base = self.get_user_base()
        if user_base == None:
            self.send_faild('TOKEN_ERROR')
            return

        if user_base['auth'] != 1:
            self.send_faild('AUTH_ERROR')
            return

        Data.update('case_info',[('id','=',data['case_id'])],{'is_show':0})
        result = {
            'case_id':data['case_id'],
        }
        self.send_ok(result)
        return



