import time

from werkzeug.security import check_password_hash, generate_password_hash

from app.http.http_tools.tools import http_tools
from data.server import Data
from common.common import common_tools as common, common_tools


class admin_tool():
    @staticmethod
    def upload_case(data,user_base):
        content = common.get_base64(data['content'].encode('utf-8'))
        content_md5 = common.get_md5(content)
        user_id = user_base['id']
        ctime = int(time.time())
        event_time = common.str_to_time(data['event_time'] + ' 00:00:00')
        title = common.get_base64(data['title'].encode('utf-8'))
        if Data.find('case_info', [('title', '=', title)]) != None:
            # self.send_faild(error.ERROR_CASE_EXIST)
            return
        params = {
            'user_id': user_id,
            'c_time': ctime,
            # 'content': content,
            'content_md5': content_md5,
            'event_time': event_time,
            'title': title,
        }
        Data.insert('case_info', params)
        # 插入主体内容
        cond = [
            ('user_id', '=', user_id),
            ('c_time', '=', ctime),
            ('content_md5', '=', content_md5)
        ]
        res = Data.find('case_info', cond)
        params = {
            'case_id': res['id'],
            'content': content
        }
        Data.insert('case_content',params)
        # 取得id，插入内容到表中
        res['content'] = content
        http_tools.split_case_info(res)
        return res

    @staticmethod
    def update_case(self):
        # id = case_id
        return

    @staticmethod
    def check_pw(user_base,pw):
        pw_md5 = common_tools.get_md5(pw)
        return check_password_hash(user_base['pwhash'], pw_md5)

    @staticmethod
    def create_pw(pw):
        pw_md5 = common_tools.get_md5(pw)
        return generate_password_hash(pw_md5)

