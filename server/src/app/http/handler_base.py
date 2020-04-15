from tornado.escape import json_decode
from tornado.web import RequestHandler
from concurrent.futures import ThreadPoolExecutor
from config import config
from error import error
from app.http.relay.relay import Relay
from config.config import thread_pool_num
import json
from config.description import description


class HandlerBase(RequestHandler):
    executor = ThreadPoolExecutor(thread_pool_num)
    print('thread_pool',thread_pool_num)

    def set_default_headers(self):
        origin = self.request.headers.get('Origin')
        if origin == None or origin == '':
            origin = '*'
        print('添加响应标头')
        self.set_header('Access-Control-Allow-Origin',origin)
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', 'X-Requested-With,Origin,Content-Type')
        for line in description:
            self.set_header(line, description[line])

    def options(self):
        print('<---------收到跨域请求，返回空值--------->')
        return self.write({})

    def get_result(self):
        '''
        返回结构基本模板
        :return:
        '''
        result = {}
        result['code'] = 0
        result['msg'] = ''
        result['data'] = {}
        return result

    def get_token(self):
        headers = self.request.headers
        token = headers.get('token')
        if token == '' or token is None:
            return None
        return token

    def get_user_base(self,character):
        '''
        获取用户基本信息
        :return:
        '''
        token = self.get_token()
        if token is None:
            print('没有携带token')
            return
        res = Relay.get_user_base(token,character)
        return res

    def login(self,user_id,character):
        res = Relay.login(user_id,character)
        return res

    def logout(self,character):
        '''
        获取post请求内容
        :return:
        '''
        token = self.get_token()
        if token == '' or token is None:
            print('没有携带token')
            return
        user_id = Relay.get_user_id_by_token(token,character)
        if user_id == None:
            return
        res = Relay.logout(user_id,character)
        return res


    def is_god(self):
        '''
        获取用户基本信息
        :return:
        '''
        token = self.get_token()
        if token == '' or token is None:
            print('没有携带token')
            return
        res = Relay.is_god(token)
        return res


    def send_ok(self, data={}):
        """
        正确信息返回
        :param data:
        :return:
        """
        result = self.get_result()
        result['data'] = data
        print('<---------请求成功，返回值--------->')
        if len(json.dumps(data))>10240:
            print()
        else:
            print(result)
        # 打印日志
        # self.set_default_headers()
        self.write(result)

    def send_faild(self, code):
        '''
        失败信息返回
        :param code:
        :return:
        '''
        result = self.get_result()
        unit = error.error_info[code]
        result['code'] = code
        result['msg'] = unit
        print('<---------请求失败，返回值--------->')
        print(result)
        # self.set_default_headers()
        self.write(json.dumps(result))

    def get_data(self):
        '''
        获取get请求内容
        :return:
        '''
        data = self.get_argument('data')
        if data is None:
            print('没有收到get参数')
            return data
        res = json.loads(data)
        print(data)
        return res

    def get_files(self, key):
        if key in self.request.files:
            file_metas = self.request.files[key][0]['body']
            return file_metas

        else:
            return None

    def get_post_data(self):
        '''
        获取post请求内容
        :return:
        '''
        # if len(self.request.body) < 1024:
        #     print(self.request.body)
        data = json_decode(self.request.body)
        if len(self.request.body) < config.logging_data_length:
            print(self.request.body)
            print('收到post数据', data)
            # res = json.loads(data)
        return data
