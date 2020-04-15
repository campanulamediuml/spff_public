from gevent import time

from common.Scheduler import IntervalTask
from common.common import common_tools
from config import weibo_config, config
from data.server import Data
from sdk.webo_sdk.weibo_api import weibo_base

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
        self.back_ground_token = Data.find('admin',[('id','=',1)])['token']

    def main_polling(self):
        self.weibo_login()
        while 1:
            self.polling()
            time.sleep(weibo_config.polling_time)

    def weibo_login(self):
        self.wb.get_auth(self.code)

    def polling(self):
        res = self.wb.get_mentioned_comment()
        for line in res['comments']:
            data = self.parse_weibo(line)
            if data != None:
                self.upload(data)

    def upload(self, data):
        url = 'http://127.0.0.1:'+ str(config.http_config['port']) + '/admin/upload'
        header = {
            'token':Data.find('admin', [('id', '=', 1)])['token']
        }
        res = common_tools.post(url, payload=data, headers=header)
        return res


    def parse_weibo(self,line):
        comment_text = line['text']
        anchor_handler_list = comment_text.split()
        if len(anchor_handler_list) < 2:
            return
        anchor_handler = anchor_handler_list[1]
        if '加入数据库' not in anchor_handler:
            return
        title = anchor_handler.split(':')[1]
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
        print(data)
        return data

    def get_event_time(self, param):
        time_list = param.split()
        # print(time_list)
        time_month = weibo_bot.monthcover[time_list[1]]
        time_string = time_list[-1]+'-'+time_month+'-'+time_list[2]
        return time_string


if __name__=='__main__':
    code = '66875c4b51b325ebc02ac6435c239b73'
    bot = weibo_bot(code)
    bot.main_polling()



