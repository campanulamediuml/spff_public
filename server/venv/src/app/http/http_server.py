from app.common.server.base import ServerBase
from app.http.relay import Relay
# 服务器


from app.http.handlers.test import test_handler
from app.http.handlers.sign_up import sign_up_handler
from app.http.handlers.login import login_handler
from app.http.handlers.upload import upload_handler
from app.http.handlers.search import search_handler
from app.http.handlers.search_time import search_by_time_handler
from app.http.handlers.search_by_case_id import search_by_case_id
from app.http.handlers.block_info import block_info
from app.http.handlers.change_pw import change_pw



class HttpServer(ServerBase):

    def __init__(self, host, port):
        ServerBase.__init__(self, host, port)
        Relay.init(self)

    def register_handles(self):
        route = [
            (r'/REQ_TEST',test_handler),
            (r'/REQ_LOGIN',login_handler),
            (r'/REQ_SIGNUP',sign_up_handler),
            # 暂不开放注册

            (r'/REQ_UPLOAD',upload_handler),
            (r'/REQ_SEARCH_BY_KEY',search_handler),
            (r'/REQ_SEARCH_BY_TIME',search_by_time_handler),
            (r'/REQ_SEARCH_BY_CASE_ID',search_by_case_id),
            (r'/REQ_BLOCK',block_info),
            (r'/REQ_CHANGE_PW',change_pw),
        ]

        # route.extend(self.register_handles_test())

        return route