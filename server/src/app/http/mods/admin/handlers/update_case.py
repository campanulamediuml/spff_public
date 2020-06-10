from tornado.concurrent import run_on_executor

from app.http.handler_base import HandlerBase
from app.http.relay.relay import Relay
# 隐藏某一条记录，需要管理员身份才能操作
from error import error


class update_info(HandlerBase):
    @run_on_executor
    def post(self):
        data = self.get_post_data()
        user_base = self.get_user_base(Relay.admin)
        if user_base == None:
            self.send_faild(error.ERROR_ADMIN_NO_LOGIN)
            return

        case_id = data['case_id']
        new_case_info = data['new_case_info']
        title = data['new_case_title']
        pic_list = data['pic_list']


        # Data.update('case_info',[('id','=',data['case_id'])],{'is_show':0})
        self.send_ok({})
        return