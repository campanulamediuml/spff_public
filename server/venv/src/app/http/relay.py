import jieba
import time
import json
from app.common import common
from app.data.server import Data


class Relay(object):
    server = None

    @staticmethod
    def init(server):
        Relay.server = server
        _initial_split_word = list(jieba.cut_for_search('服务器操作'))
        Relay.is_any_user()
        # 创建初始用户

# 服务器核心操作放在这里
    @staticmethod
    def is_any_user():
        res = Data.find('user',[('id','!=',0)])
        if res != None:
            return

        params = {
            'user_name':'admin',
            'passwd':common.get_md5('admin123456'),
            'join_time':int(time.time()),
            'uuid':100000,
            'invite_id':0,
            'nickname':json.dumps('admin'),
            'auth':1
        }

        Data.insert('user',params)
        print('插入初始用户')







