import json
import time

from app.http.relay.relay import Relay
from common.Scheduler import IntervalTask
from common.common import common_tools
from config import weibo_config, config
from data.server import Data


class weibo_base(object):
    client_id=weibo_config.client_id
    client_secret=weibo_config.client_secret
    app_uri=weibo_config.app_uri

    def __init__(self):
        self.access_token = '2.00Vq3_GCtnLAMB4e27fc0d619_X2yD'
        # self.access_token = ''
        self.end_time = 157679999
        self.user_uid = '1925539735'

    def get_auth(self,code):
        request_url = 'https://api.weibo.com/oauth2/access_token'
        request_params = {
            'client_id':weibo_base.client_id,
            'client_secret':weibo_base.client_secret,
            'grant_type':'authorization_code',
            'code':code,
            'redirect_uri':weibo_base.app_uri
        }
        request_url = request_url+'?'+common_tools.dict_to_url_params(request_params)
        res = common_tools.post(request_url,show_data=False,show_headers=False)
        res = json.loads(res)
        self.access_token = res["access_token"]
        self.end_time = res['expires_in']
        self.user_uid = res['uid']
        return

    def get_mentioned_weibo(self):
        request_url = 'https://api.weibo.com/2/statuses/mentions.json'
        request_params = {
            'access_token': self.access_token,
        }
        request_url = request_url + '?' + common_tools.dict_to_url_params(request_params)
        res = common_tools.get(request_url,show_data=False,show_headers=False)
        res = json.loads(res)
        if 'error' in res:
            return
        return res

    def get_mentioned_comment(self):
        request_url = 'https://api.weibo.com/2/comments/mentions.json'
        request_params = {
            'access_token': self.access_token,
        }
        request_url = request_url + '?' + common_tools.dict_to_url_params(request_params)
        res = common_tools.get(request_url,show_data=False,show_headers=False)
        res = json.loads(res)
        if 'error' in res:
            return
        return res

class weibo_bot(object):
    monthcover = {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12',
    }

    def __init__(self,code):
        self.wb_img_url='http://wx2.sinaimg.cn/large/'
        self.wb = weibo_base()
        self.code = code
        # self.back_ground_token = Data.find('admin',[('id','=',1)])['token']

    def main_polling(self):
        self.weibo_login()
        # while 1:
        #     self.polling()
        IntervalTask(weibo_config.polling_time,self.polling)

    def weibo_login(self):
        self.wb.get_auth(self.code)

    def polling(self):
        try:
            res = self.wb.get_mentioned_comment()
            for line in res['comments']:
                data = self.parse_weibo(line)
                if data != None:
                    res = self.upload(data)
                    if res != None:
                        if json.loads(res)['code'] == 0:
                            print(data)
        except Exception as e:
            print(str(e))
            return

    def upload(self, data):
        url = 'http://127.0.0.1:'+ str(config.http_config['port']) + '/player/upload'
        header = {
            'token':Data.find(Relay.player, [('id', '=', 1)])['token']
        }
        res = common_tools.post(url, payload=data, headers=header,show_data=False,show_headers=False)
        return res


    def parse_weibo(self,line):
        comment_text = line['text']
        anchor_handler_list = comment_text.split()
        if len(anchor_handler_list) < 2:
            return
        anchor_handler = anchor_handler_list[1]
        if '加入数据库' not in anchor_handler:
            return
        title_list = anchor_handler.split(':')
        if len(title_list) < 2:
            return
        title = ':'.join(title_list[1:])
        origin_weibo = line['status']
        content = origin_weibo['text']
        pic_list = []
        event_time = self.get_event_time(origin_weibo['created_at'])
        for i in origin_weibo['pic_ids']:
            pic_list.append(self.wb_img_url+i+'.jpg')
        data = {
            'event_time': event_time,
            'title': title,
            'content': content,
            'post_items': pic_list,
        }
        # print(data)
        return data

    def get_event_time(self, param):
        time_list = param.split()
        # print(time_list)
        time_month = weibo_bot.monthcover[time_list[1]]
        time_string = time_list[-1]+'-'+time_month+'-'+time_list[2]
        return time_string



def run(code):
    bot = weibo_bot(code)
    bot.main_polling()

if __name__=='__main__':
    wb = weibo_base()

