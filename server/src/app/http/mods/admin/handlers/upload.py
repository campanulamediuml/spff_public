from tornado.concurrent import run_on_executor

from app.http.handler_base import HandlerBase
from app.http.mods.admin.admin_tools import admin_tool
from app.http.relay.relay import Relay
from app.http.http_tools.tools import http_tools
# from config.config import


from error import error

strip_word_list = ['\n',' ']

class upload_handler(HandlerBase):
    @run_on_executor
    def post(self):
        data = self.get_post_data()

        user_base = self.get_user_base(Relay.admin)
        if user_base == None:
            print('token错误')
            self.send_faild(error.ERROR_FAIL)
            return

        res = admin_tool.upload_case(data,user_base)
        # 上传信息
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
