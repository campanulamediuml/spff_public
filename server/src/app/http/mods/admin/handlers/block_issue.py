from tornado.concurrent import run_on_executor

from app.http.handler_base import HandlerBase
from app.http.relay.relay import Relay
from common.constant.case_constant import status_can_show, status_canot_show, status_verified
from data.server import Data
# 隐藏某一条记录，需要管理员身份才能操作
from error import error


class block_info(HandlerBase):
    @run_on_executor
    def post(self):
        data = self.get_post_data()
        user_base = self.get_user_base(Relay.admin)
        if user_base == None:
            self.send_faild(error.ERROR_ADMIN_NO_LOGIN)
            return
        params = {
            'is_show': status_canot_show,
            'is_verified':status_verified
        }


        Data.update('case_info',[('id','=',data['case_id'])],params)
        self.send_ok({})
        return

class unblock_info(HandlerBase):
    @run_on_executor
    def post(self):
        data = self.get_post_data()
        user_base = self.get_user_base(Relay.admin)
        if user_base == None:
            self.send_faild(error.ERROR_ADMIN_NO_LOGIN)
            return

        Data.update('case_info',[('id','=',data['case_id'])],{'is_show':status_can_show })
        self.send_ok({})
        return
