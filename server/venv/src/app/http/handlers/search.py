from app.http.handler_base import HandlerBase
from app.data.server import Data
from app.common import common
import time
import json

class search_handler(HandlerBase):
    def get(self):
        data = self.get_data()
        keyword_list = data['keyword_list']

        if keyword_list == []:
            self.send_faild('NEED_WORD')
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
            res = Data.find('case_info',[('id','=',case_id),('is_show','=',1)])
            # 需要能显示的才可以看
            if res == None:
                continue
            else:
                case_info = {
                    'case_id':res['id'],
                    'title':res['title']
                }
                title_list.append(case_info)
                continue

        result = {
            'keyword_list':keyword_list,
            'result':title_list
        }
        # 关键词搜索

        self.send_ok(result)
        return

    # 根据关键词进行搜索           
