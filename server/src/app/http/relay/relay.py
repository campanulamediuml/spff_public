import time

from common.common import common_tools
from data.server import Data
import jieba

class Relay(object):
    server = None
    player_token_dict = {}
    admin_token_dict = {}
    token_dict_collection = {
        'player':player_token_dict,
        'admin':admin_token_dict
    }

    @staticmethod
    def server_init(server):
        Relay.server = server
        _initial_split_word = list(jieba.cut_for_search('server_execute'))
        print('init split word execute')
        # 创建初始用户
        for character in Relay.token_dict_collection:
            all_user = Data.select(character, [('id', '!=', 0)])
            if all_user != None:
                for line in all_user:
                    Relay.token_dict_collection[character][line['id']] = ''
        return
        # 初始化系统缓存内用户信息
        # IntervalTask(1,Relay.refresh_token)
    # 服务器核心操作放在这里
    @staticmethod
    def test():
        pass

    @staticmethod
    def create_token():
        nonce_string = common_tools.create_rand_string(12)+str(time.time())
        token = common_tools.get_md5(nonce_string)
        return token

    @staticmethod
    def get_token_dict(key_name):
        res = Relay.token_dict_collection[key_name]
        return res
        # 根据用户角色取得不同的管理器
    @staticmethod
    def add_token(user_dict,user_id,token):
        user_dict[user_id] = token
        return
    @staticmethod
    def remove_token(user_dict,user_id):
        if user_id in user_dict:
            user_dict[user_id] = ''
        return
    # 清除token

    @staticmethod
    def login(user_id, character):
        user_dict = Relay.token_dict_collection[character]
        token = Relay.create_token()
        Data.update(character, [('id', '=', user_id)], {'token': token})
        Relay.add_token(user_dict,user_id,token)
        return token
        # 登录
    @staticmethod
    def logout(user_id,character):
        user_dict = Relay.token_dict_collection[character]
        Relay.remove_token(user_dict,user_id)
        Data.update(character,[('id','=',user_id)],{'token':''})
        return
        # 退出
    @staticmethod
    def get_user_base(token,character):
        token_dict = Relay.token_dict_collection[character]
        for user_id in token_dict:
            if token_dict[user_id] == token:
                res = Data.find(character,[('id','=',user_id)])
                return res
        # =============优先查找内存=============
        res = Data.find(character, [('token', '=', token)])
        if res != None:
            return res
        # 之后查找token
        # Relay.update_admin_token_timeout(token)
        return
    # 查找用户信息

    @staticmethod
    def is_god(token):
        if token in Relay.admin_token_dict:
            return True

        res = Data.find('admin', [('token', '=', token)])
        if res is None:
            return False

        return True
    # 判断是不是超级管理员
    @staticmethod
    def get_user_id_by_token(token,character):
        user_dict = Relay.token_dict_collection[character]
        for user_id in user_dict:
            if user_dict[user_id] == token:
                return user_id
        return





