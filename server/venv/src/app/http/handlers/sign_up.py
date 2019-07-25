from app.http.handler_base import HandlerBase
from app.data.server import Data
from app.common import common
import time
import json

class sign_up_handler(HandlerBase):
    def get(self):
        data = self.get_data()

        if data['pw1'] != data['pw2']:
            self.send_faild('PW_NOT_SAME')
            return 

        if data['invite_token'] == '':
            self.send_faild('NO_TOKEN')
            return
        # 需要传入邀请者token作为参数

        res = Data.find('user',[('user_name','=',data['username'])])
        if res != None:
            self.send_faild('ACCOUNT_HAD')
            return 

        inviter = Data.find('user',[('token','=',data['invite_token'])])
        if inviter == None:
            self.send_faild('NO_TOKEN')
            return 

        # 邀请码处理

        params = {
            'user_name':data['username'],
            'passwd':common.get_md5(data['pw2']),
            'join_time':int(time.time()),
            'uuid':self.create_uuid(),
            'invite_id':inviter['id'],
            'nickname':json.dumps(data['nickname'])
        }

        Data.insert('user',params)
        Data.update('user',[('id','=',inviter['id'])],{'token':''})
        # 插入新的数据，为了安全，更新一次token


        conditions = [
            ('user_name','=',data['username']),
            ('passwd','=',common.get_md5(data['pw2']))
        ]

        res = Data.find('user',conditions)
        token = self.get_token(res)

        result = {
            'token':token
        }

        Data.update('user',conditions,result)
        # 插入token

        self.send_ok(result)
        return 

    # 注册




