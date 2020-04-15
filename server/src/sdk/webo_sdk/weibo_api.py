import json

from common.common import common_tools
from config import weibo_config


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





if __name__=='__main__':
    wb = weibo_base()
    # # wb.get_auth('720a029423e952a479971beb1f74c192')
    # print(common_tools.time_to_str(wb.end_time))
    # res = wb.get_mentioned_comment()
    # for line in res['comments']
    #     comment_text = line['text']
    #     anchor_handler = comment_text.split()
    #     # if '加入数据库' in anchor_handler:
    #     title = comment_text.split()
    #     origin_weibo = line['status']
    #     content = origin_weibo['text']
    #     # pic_list =pic
    #     if len(origin_weibo['pic_ids']) != 0:
    #         # print(origin_weibo)
    #         print(line['text'])
    #         # print(origin_text)
    #         print(origin_weibo['pic_ids'])
    #         print(origin_weibo['original_pic'])
    #
    #     print('=========================')

