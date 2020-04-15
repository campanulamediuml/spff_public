from tornado.concurrent import run_on_executor

from app.http.handler_base import HandlerBase
from data.server import Data
from common.common import common_tools as common
import time
import json
from app.http.http_tools.tools import http_tools
# from config.config import
import requests
import os
import jieba

from error import error

strip_word_list = ['\n',' ']

class upload_handler(HandlerBase):
    @run_on_executor
    def post(self):
        data = self.get_post_data()
        # try:
        # character = data['character']
        user_base = self.get_user_base('admin')
        if user_base == None:
            print('token错误')
            self.send_faild(error.ERROR_FAIL)
            return

        content = common.get_base64(data['content'].encode('utf-8'))
        content_md5 = common.get_md5(content)
        user_id = user_base['id']
        ctime = int(time.time())
        event_time = common.str_to_time(data['event_time']+' 00:00:00')
        title = common.get_base64(data['title'].encode('utf-8'))
        if Data.find('case_info',[('title','=',title)]) != None:
            self.send_faild(error.ERROR_CASE_EXIST)
            return
        params = {
            'user_id':user_id,
            'c_time':ctime,
            'content':content,
            'content_md5':content_md5,
            'event_time':event_time,
            'title':title,
        }
        Data.insert('case_info',params)
        # 插入主体内容
        # self.write_event_post_item()
        cond = [
            ('user_id','=',user_id),
            ('c_time','=',ctime),
            ('content_md5','=',content_md5)
        ]
        res = Data.find('case_info',cond)
        http_tools.split_case_info(res)
        # 创建关键词索引
        # self.write_event_post_item(data,res)
        if res != None:
            self.send_ok({})
            http_tools.write_event_post_item(data,res)
            print('download_done!')
            return
        else:
            self.send_faild(error.ERROR_FAIL)
            return
