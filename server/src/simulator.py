import json
import requests

from common.common import common_tools
from config import config

debug = 0
# debug=1为操作本地服务端

if debug == 0:
    main_url = 'http://spffapi.campanula.wang'
else:
    main_url = 'http://127.0.0.1:'+ str(config.http_config['port'])

class simulator(object):
    def __init__(self):
        self.headers = {
            'token':'',
        }
        
    def recver(self,data):
        if data == None:
            return
        data = json.loads(data)
        if data['code'] != 0:
            print(data['msg'])
            return
        return data['data']

    def admin_login(self,user_name,pw):
        url = main_url + '/admin/login'
        data = {
            'username':user_name,
            'pswd':pw,
        }
        res = common_tools.post(url, payload=data, headers=self.headers,show_headers=False,show_data=False)
        data = self.recver(res)
        if data == None:
            return
        self.headers['token'] = data['token']
        return data
    # 管理员登录

    def online_admin(self):
        url = main_url + '/test/onlineadmin'
        res = common_tools.post(url, headers=self.headers,show_headers=False,show_data=False)
        # print(res)
        return self.recver(res)
    # 查看在线管理员

    def admin_logout(self):
        url = main_url + '/admin/logout'
        res = common_tools.post(url, headers=self.headers,show_headers=False,show_data=False)
        # print(res)
        return self.recver(res)
    # 管理员退出

    def upload(self,data):
        url = main_url + '/admin/upload'
        res = common_tools.post(url, payload=data, headers=self.headers,show_headers=False,show_data=False)
        return self.recver(res)
    # 管理员上传信息

    def search_by_kw(self,data):
        url = main_url + '/uni/searchbykw'
        res = common_tools.post(url, payload=data, headers=self.headers,show_headers=False,show_data=False)
        return self.recver(res)
    # 根据关键词查询

    def search_by_time(self,data):
        url = main_url + '/uni/searchbytime'
        res = common_tools.post(url, payload=data, headers=self.headers,show_headers=False,show_data=False)
        return self.recver(res)
    # 根据时间查询

    def search_by_id(self,data):
        url = main_url + '/uni/searchbyid'
        res = common_tools.post(url, payload=data, headers=self.headers,show_headers=False,show_data=False)
        return self.recver(res)
    # 根据id获取事件的关键信息

    def check_unverified_case(self):
        url = main_url + '/admin/checkunverifiedcase'
        res = common_tools.post(url, headers=self.headers,show_headers=False,show_data=False)
        return self.recver(res)

    def verify_case_by_id(self,data):
        url = main_url + '/admin/verifycase'
        res = common_tools.post(url, payload=data, headers=self.headers, show_headers=False, show_data=False)
        return self.recver(res)

    def block_case(self,data):
        url = main_url+'/admin/block'
        res = common_tools.post(url, payload=data, headers=self.headers, show_headers=False, show_data=False)
        return self.recver(res)

    def unblock_case(self,data):
        url = main_url+'/admin/unblock'
        res = common_tools.post(url, payload=data, headers=self.headers, show_headers=False, show_data=False)
        return self.recver(res)

# ===================模拟客户端=======================

def create_upload_info():
    data = {
        'event_time':'2020-04-13',
        'title': '#鲍毓明目前处于取保候审# 女孩现在状态十分差',
        'content':'4月13日，当事女孩的律师表示，星星状态很差，患有重度抑郁焦虑及创伤后应急障碍。鲍某某目前处在取保候审状态↓↓且其专职律师身份兼任企业高管或违规，#北京司法局介入调查鲍毓明#。',
        'post_items':[
        ]
    }
    return data
# 测试信息

def create_search_info():
    data = {
        'keyword_list':[
            '鲍某某','公安部'
        ]
    }
    return data
# 测试信息，公安部鲍某某关键词查询

def create_search_time():
    data = {
        'limit_year_time':'2020'
    }
    return data
# 2020年按时间查询

def create_case_id(case_id):
    data = {
        'case_id':str(case_id)
    }
    return data
# 按照id获取关键信息

if __name__=='__main__':
    sim = simulator()
    login_info = sim.admin_login('','')
    print(login_info)
    # 管理员身份登录
    res = sim.check_unverified_case()
    if res != None:
        for i in res['result_list']:
            print(i)
            print('==========================')
    # 查看未审核信息
    data = create_case_id(case_id=101)
    res = sim.search_by_id(data)
    print(res)
    # # 根据id查找信息
    # data = create_case_id(case_id=93)
    # res = sim.verify_case_by_id(data)
    # print(res)
    # # 根据id进行确认操作
    # data = create_case_id(case_id=57)
    # res = sim.unblock_case(data)
    # print(res)
    # # 屏蔽操作
    # # 根据id进行确认操作
    # data = create_case_id(case_id=104)
    # res = sim.block_case(data)
    # print(res)
    # 屏蔽操作
# =====================================================

    # case_id =
    # data = create_upload_info()
    # sim.upload(data)
    # data = create_search_id(40)
    # res = sim.search_by_id(data)
    # print(res)
    # #
    data = create_search_time()
    res = sim.search_by_time(data)
    print(res)
    for i in res['result_list']:
        print(i['case_id'],i['title'])
        print('===========================================')