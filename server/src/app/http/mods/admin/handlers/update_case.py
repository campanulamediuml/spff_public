from tornado.concurrent import run_on_executor

from app.http.handler_base import HandlerBase
from app.http.http_tools.tools import http_tools
from app.http.mods.admin.admin_tools import admin_tool
from app.http.relay.relay import Relay
# 隐藏某一条记录，需要管理员身份才能操作
from common.constant.case_constant import status_canot_show
from data.server import Data
from error import error


class update_info(HandlerBase):
    @run_on_executor
    def post(self):
        data = self.get_post_data()
        user_base = self.get_user_base(Relay.admin)
        if user_base == None:
            self.send_faild(error.ERROR_ADMIN_NO_LOGIN)
            return

        res = admin_tool.upload_case(data, user_base)
        data_id_old = data['case_id']
        # 上传信息，并且block旧的信息
        Data.update('case_info',[('id','=',data_id_old)],{'is_show':status_canot_show })
        if res != None:
            self.send_ok({})
            http_tools.write_event_post_item(data, res)
            print('download_done!')
            return
        else:
            self.send_faild(error.ERROR_FAIL)
            return
