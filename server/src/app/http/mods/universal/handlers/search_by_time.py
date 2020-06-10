from tornado.concurrent import run_on_executor

from app.http.handler_base import HandlerBase
from app.http.http_tools.tools import http_tools
from app.http.relay.relay import Relay
from common.constant.case_constant import status_can_show, status_verified
from data.server import Data
from common.common import common_tools as common
import time
import json

from error import error


class search_by_time_handler(HandlerBase):
    @run_on_executor
    def post(self):
        data = self.get_post_data()
        if self.get_user_base(Relay.admin) != None:
            print(self.get_user_base(Relay.admin))
            cond = []
        else:
            cond = [('is_show', '=', status_can_show ), ('is_verified', '=', status_verified)]

        search_time = data['limit_year_time']
        if search_time != '':
            search_time_stamp_start = common.str_to_time(str(search_time)+'-01-01 00:00:00')
            search_time_stamp_end = common.str_to_time(str(search_time)+'-12-31 23:59:59')
        else:
            search_time_stamp_start = 0
            search_time_stamp_end = int(time.time())

        condition = [
            ('event_time','>',search_time_stamp_start),
            ('event_time','<',search_time_stamp_end),
        ] + cond

        result_list = http_tools.get_case_list_by_cond(condition)

        if result_list == None:
            self.send_faild(error.ERROR_NO_RESULT)
            return

        result = {
            'result_list':result_list
        }

        # print(result)

        self.send_ok(result)
        return

        # 按时间进行搜索