from app.http.handler_base import HandlerBase
from app.data.server import Data
from app.common import common
import time
import json

class search_by_time_handler(HandlerBase):
    def get(self):
        data = self.get_data()
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
            ('is_show','=',1),
        ]

        res = Data.select('case_info',condition)
        result_list = []

        if res == None:
            self.send_faild('NO_RECORD')
            return


        for line in res:
            info_line = {
                'ctime':common.time_to_str(line['ctime']).split()[0],
                'title':line['title'],
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