from app.http.handler_base import HandlerBase
from app.data.server import Data
from app.common import common
import time
import json     


class search_by_case_id(HandlerBase):
    def get(self):
        data = self.get_data()
        case_id = data['case_id']
        line = Data.find('case_info',[('id','=',case_id),('is_show','=',1)])
        if line == None:
            self.send_faild('NO_RECORD')
            return
        
        info_line = {
            'case_id':line['id'],
            'content':json.loads(line['content']),
            'ctime':common.time_to_str(line['ctime']).split()[0],
            'title':line['title'],
            'uploader_info':self.get_uploader_info(line['user_id']),
            'post_items':self.get_post_items(line['id']),

        }
    
        result = info_line

        # print(result)

        self.send_ok(result)
        return


    def get_uploader_info(self,user_id):
        # 获取上传者信息
        res = Data.find('user',[('id','=',user_id)])
        result = {
            'nickname':json.loads(res['nickname']),
            'uuid':res['uuid']
        }
        return result

    def get_post_items(self,case_id):
        # 获取案子相关附件
        result = []
        res = Data.select('case_post_item',[('case_id','=',case_id)])
        if res != None:
            for line in res:
                result.append(line['post_item'])

        return result