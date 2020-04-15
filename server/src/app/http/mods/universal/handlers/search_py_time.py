from tornado.concurrent import run_on_executor

from app.http.handler_base import HandlerBase
from data.server import Data
from common.common import common_tools as common
import time
import json

class search_by_time_handler(HandlerBase):
    @run_on_executor
    def post(self):
        data = self.get_post_data()
        if self.get_user_base('admin') != None:
            shown = ('is_show','>',-1)
        else:
            shown = ('is_show','=',1)

        search_time = data['limit_year_time']
        if search_time != '':
            search_time_stamp_start = common.str_to_time(str(search_time)+'-01-01 00:00:00')
            search_time_stamp_end = common.str_to_time(str(search_time)+'-12-31 23:59:59')
        else:
            search_time_stamp_start = 0
            search_time_stamp_end = 999999999

        condition = [
            ('event_time','>',search_time_stamp_start),
            ('event_time','<',search_time_stamp_end),
            shown
        ]

        res = Data.select('case_info',condition)
        result_list = []

        if res == None:
            self.send_faild('NO_RECORD')
            return

        for line in res:
            info_line = {
                'c_time':common.time_to_str(line['c_time']).split()[0],
                'title':common.decode_base64(line['title']),
                'case_id':line['id']
            }
            result_list.append(info_line)

        result = {
            'result_list':result_list
        }

        # print(result)

        self.send_ok(result)
        return

        # 按时间进行搜索