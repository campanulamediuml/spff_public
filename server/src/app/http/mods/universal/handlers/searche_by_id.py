from tornado.concurrent import run_on_executor

from app.http.handler_base import HandlerBase
from app.http.http_tools.tools import http_tools as tools
from app.http.relay.relay import Relay

from error import error


class search_by_case_id(HandlerBase):
    @run_on_executor
    def post(self):
        data = self.get_post_data()
        case_id = data['case_id']
        if self.get_user_base(Relay.admin) != None:
            character = 'admin'
        else:
            character = 'player'

        result = tools.search_case_by_case_id(case_id, character)
        if result == None:
            self.send_faild(error.ERROR_NO_RESULT)
            return
        self.send_ok(result)
        return