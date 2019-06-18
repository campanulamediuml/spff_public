from app.http.handler_base import HandlerBase
from app.data.server import Data

class test_handler(HandlerBase):
    def get(self):
        res = Data.find('test',[('id','!=',0)])
        self.send_ok(res)