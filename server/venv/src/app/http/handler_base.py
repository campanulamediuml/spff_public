from tornado.web import RequestHandler
from tornado.escape import json_decode
from app.http.error_code import ERROR_CODE
from app.data.server import Data

import json
import time
from app.common import common

class HandlerBase(RequestHandler):


    
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')

    def get_result(self):
        '''
        返回结构基本模板
        :return:
        '''
        result = {}
        result['status'] = 0
        result['msg'] = ''
        result['data'] = {}
        return result

    def get_user_base(self):
        '''
        获取用户基本信息
        :return:
        '''
        token = self.get_argument('token')
        # print(token)
        conditions = []
        if token == '':
            # 如果不存在token
            return None


        conditions.append(('token', '=', token))

        user_data = Data.find('user', conditions)
        
        return user_data


        # return user_data


    def send_ok(self, data = {}):
        '''
        正确信息返回
        :param data:
        :return:
        '''
        result = self.get_result()
        result['data'] = data
        self.write(result)

    def send_faild(self, code):
        '''
        失败信息返回
        :param code:
        :return:
        '''
        result = self.get_result()
        unit = ERROR_CODE[code]
        result['status'] = unit[0]
        result['msg'] = unit[1]
        self.write(json.dumps(result))

    def get_data(self):
        '''
        获取请求内容
        :return:
        '''
        data = self.get_argument('data')
        res = json.loads(data)
        return res

    def get_post_data(self):
        data = json_decode(self.request.body)
        # print(data)
        return data

    def get_token(self,res):

        # 生成该用户的token

        uuid_string = str(res['uuid'])
        user_id_string = str(res['id'])
        username_string = str(res['user_name'])
        time_string = str(int(time.time()))

        token = common.get_md5(uuid_string+user_id_string+username_string+time_string)

        return token 


    def create_uuid(self):
        # 生成一个uuid
        uuid_list = []
        all_number = []
        for i in range(100000,999999):
            all_number.append(i)

        res = Data.select('user',[('id','!=',0)])
        if res == None:
            pass
        else:
            for i in res:
                uuid_list.append(i['uuid'])

        for uuid in uuid_list:
            all_number.remove(uuid)

        return all_number[0]













