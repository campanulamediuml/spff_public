from tornado.concurrent import run_on_executor

from app.http.handler_base import HandlerBase
from app.http.relay.relay import Relay
from common.constant.case_constant import status_verified, status_can_show
from data.server import Data
from common.common import common_tools as common, common_tools
import time
import json

from error import error


class search_handler(HandlerBase):
    @run_on_executor
    def post(self):
        data = self.get_post_data()
        keyword_list = data['keyword_list']
        if self.get_user_base(Relay.admin) != None:
            cond = []
        else:
            cond = [('is_show','=',status_can_show ),('is_verified','=',status_verified)]

        if keyword_list == []:
            self.send_faild(error.ERROR_PARAM)
            return

        case_id_list = []
        for keyword in keyword_list:
            keyword_md5 = common.get_md5(keyword)
            res = Data.select('case_search_index',[('keyword_md5','=',keyword_md5)])
            if res == None:
                continue
            else:
                for case in res:
                    case_id_list.append(case['case_id'])
                continue

        case_id_list = list(set(case_id_list))
        print(case_id_list)

        title_list = []
        for case_id in case_id_list:
            res = Data.find('case_info',[('id','=',case_id)]+cond)
            # 需要能显示的才可以看
            if res == None:
                continue
            else:
                case_info = {
                    'case_id':res['id'],
                    'title':common.decode_base64(res['title'])
                }
                title_list.append(case_info)
                continue
        title_list = list(reversed(title_list))

        result = {
            'keyword_list':keyword_list,
            'result':title_list
        }
        # 关键词搜索

        self.send_ok(result)
        return

