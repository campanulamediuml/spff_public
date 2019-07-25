from app.http.handler_base import HandlerBase
from app.data.server import Data
from app.common import common
import time
import json
from config import SERVER
import requests
import os
import jieba

strip_word_list = ['\n',' ']

class upload_handler(HandlerBase):
    def post(self):
        data = self.get_post_data()
        user_base = self.get_user_base()

        content = json.dumps(data['content'])
        # content = content.replace('\\','\\\\') # 不确定是否需要
        content_md5 = common.get_md5(content)


        user_id = user_base['id']
        ctime = int(time.time())
        event_time = common.str_to_time(data['event_time']+' 00:00:00')
        title = data['title']

        # Data.find('case_info',[('content_md5','=',content_md5)])


        params = {
            'user_id':user_id,
            'ctime':ctime,
            'content':content,
            'content_md5':content_md5,
            'event_time':event_time,
            'title':title,
        }

        Data.insert('case_info',params)
        # self.write_event_post_item()

        cond = [
            ('user_id','=',user_id),
            ('ctime','=',ctime),
            ('content_md5','=',content_md5)
        ]

        res = Data.find('case_info',cond)
        self.split_case_info(res)
        # 创建关键词索引

        # self.write_event_post_item(data,res)

        if res != None:
            self.send_ok({})
            self.write_event_post_item(data,res)
            print('download_done!')
            return
        else:
            self.send_faild({'INSERT_FAIL'})
            return

    def write_event_post_item(self,data,res):
        for item in data['post_items']:
            item_url = self.get_post_item(item)
            params = {
                'case_id':res['id'],
                'post_item':item_url,
                'ctime':int(time.time()),
                'raw_url':item,
            }

            Data.insert('case_post_item',params)

    def get_post_item(self,item_url):
        file_tail = item_url.split('/')[-1].split('.')[-1]

        if file_tail in SERVER['file_name']:
            # 图片文件
            r = requests.get(item_url)
            content = str(r.content)
            file_name = common.get_md5(content)

            running_path =os.path.abspath('..')
            path = running_path.split('/')
            client_path = path[:-2]
            client_path.append('client/web_index/post_items/')

            client_path = '/'.join(client_path)

            open(client_path+file_name+'.'+file_tail,'wb').write(r.content)
            item_url = SERVER['URL']+file_name+'.'+file_tail

        return item_url

        # 存入本地

    def split_case_info(self,case):
        title = case['title']
        content = json.loads(case['content'])
        title_list = list(jieba.cut_for_search(title))
        content_list = list(jieba.cut_for_search(content))

        case_list = title_list+content_list
        case_word_list = list(set(case_list))

        # print(case_list)
        for word in case_word_list:
            if word not in strip_word_list:
                word_md5 = common.get_md5(word)
                res = Data.find('case_search_index',[('case_id','=',case['id']),('keyword_md5','=',word_md5)])
                if res != None:
                    # print('已经存在')
                    continue
                params = {
                    'case_id':case['id'],
                    'keyword':json.dumps(word),
                    'keyword_md5':word_md5
                }
                Data.insert('case_search_index',params)
                continue
            else:
                continue

    # 上传数据












