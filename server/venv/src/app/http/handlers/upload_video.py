from app.http.handler_base import HandlerBase
from app.data.server import Data
from app.common import common
import time
import json

class upload_video(HandlerBase):
    def get(self):
        data = self.get_data()
        return