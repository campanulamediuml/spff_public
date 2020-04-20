import json
import time

from common.common import common_tools
from config import config

# main_url = 'http://spff.campanula.wang'
main_url = 'http://127.0.0.1:'+ str(config.http_config['port'])

class simulator(object):
    def __init__(self):
        self.headers = {
            'token':'d963f3b7206f122699be97b0ae1ea3f0',
            'Origin':'lo'
        }
        # self.token = '27d105bee92175a2707d8a2534481a8f'

    def admin_login(self,user_name,pw):
        url = main_url + '/admin/login'
        data = {
            'username':user_name,
            'pswd':pw,
        }
        res = json.loads(common_tools.post(url,payload=data,headers=self.headers))
        # print(res)
        self.headers['token'] = res['data']['token']
        return res

    def online_admin(self):
        url = main_url + '/test/onlineadmin'
        res = json.loads(common_tools.get(url,headers=self.headers))
        # print(res)
        return res

    def admin_logout(self):
        url = main_url + '/admin/logout'
        res = common_tools.post(url,headers=self.headers)
        # print(res)
        return res

    def upload(self,data):
        url = main_url + '/admin/upload'
        res = common_tools.post(url, payload=data ,headers=self.headers)
        return res

    def search_by_kw(self,data):
        url = main_url + '/uni/searchbykw'
        res = common_tools.post(url, payload=data, headers=self.headers)
        return res

    def search_by_time(self,data):
        url = main_url + '/uni/searchbytime'
        res = common_tools.post(url, payload=data, headers=self.headers)
        return res

    def search_by_id(self,data):
        url = main_url + '/uni/searchbyid'
        res = common_tools.post(url, payload=data, headers=self.headers)
        return res


def create_upload_info():
    data = {
        'event_time':'2020-04-13',
        'title': '#鲍毓明目前处于取保候审# 女孩现在状态十分差',
        'content':'4月13日，当事女孩的律师表示，星星状态很差，患有重度抑郁焦虑及创伤后应急障碍。鲍某某目前处在取保候审状态↓↓且其专职律师身份兼任企业高管或违规，#北京司法局介入调查鲍毓明#。',
        'post_items':[
        ]
    }
    return data

def create_search_info():
    data = {
        'keyword_list':[
            '鲍某某','公安部'
        ]
    }
    return data

def create_search_time():
    data = {
        'limit_year_time':'2020'
    }
    return data

def create_search_id():
    data = {
        'case_id':'1'
    }
    return data

if __name__=='__main__':

    sim = simulator()
    login_info = sim.admin_login('','')
    print(login_info)
    # data = create_upload_info()
    # sim.upload(data)
    # data = create_search_info()
    # res = sim.search_by_kw(data)
    #
    data = create_search_time()
    res = json.loads(sim.search_by_time(data))

    #
    # data = create_search_id()
    # res = sim.search_by_id(data)
    #


    # print()
    for i in res['data']['result_list']:
        print(i['case_id'],i['title'])