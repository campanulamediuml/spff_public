from tornado.concurrent import run_on_executor

from app.http.handler_base import HandlerBase
from app.http.http_tools.tools import http_tools
from app.http.relay.relay import Relay
from common.constant.case_constant import status_unverify, status_verified
from data.server import Data

from error import error
# 查询还未确认的条目

class check_case_handler(HandlerBase):
    @run_on_executor
    def post(self):
        admin_info = self.get_user_base(character=Relay.admin)
        if admin_info ==None:
            self.send_faild(error.ERROR_ADMIN_NO_LOGIN)
            return
        cond = [('is_verified', '=', status_unverify)]
        res = http_tools.get_case_list_by_cond(cond)

        if res == None:
            self.send_faild(error.ERROR_NO_RESULT)
            return

        result = {
            'result_list':res
        }
        self.send_ok(result)
        return

class verify_case_handler(HandlerBase):
    @run_on_executor
    def post(self):
        admin_info = self.get_user_base(character=Relay.admin)
        if admin_info == None:
            self.send_faild(error.ERROR_ADMIN_NO_LOGIN)
            return
        data = self.get_post_data()
        case_id = data['case_id']
        # case_status = data['case_status']
        res = Data.find('case_info',[('id','=',case_id),('is_verified','=',status_unverify)])
        if res == None:
            self.send_faild(error.ERROR_NO_RESULT)
            return
        params = {
            'is_verified':status_verified,
            'verifyer':admin_info['id']
        }
        Data.update('case_info',[('id','=',case_id),('is_verified','=',status_unverify)],params)
        if Data.find('case_info',[('id','=',case_id),('is_verified','=',status_verified)]) == None:
            self.send_faild(error.ERROR_FAIL)
            return

        self.send_ok({})
        return


