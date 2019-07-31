import requests
import json
from test_config.config import config


class client(object):

    def __init__(self,username,passwd):
        self.token = ''
        self.username = username
        self.pw = passwd

    def login(self):
        url ='http://'+config['server_host']+'/REQ_LOGIN?data=%7B%22type%22:2,%22username%22:%22'+self.username+'%22,%22pw%22:%22'+self.pw+'%22%7D'
        r = requests.get(url)
        return_data = json.loads(r.content)
        print(return_data)
        if return_data['status'] == 0:
            self.token = return_data['data']['token']
        return 

    def update_token(self):
        self.login()
        return self.token
        

