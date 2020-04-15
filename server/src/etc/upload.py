import requests
import json
from test_login import client
from test_config.config import config


username = config['username']
pw = config['pw']

def upload():
    login_session = client(username,pw)
    token = login_session.update_token()
    content = {
        'content':'''
        普宁红领巾实验学校老师性侵学生，还拍了照片，家长多次找到学校却一直敷衍了事，请记住这个人渣，孩子是我们的底线不容许践踏 ​​​​
        ''',
        'title':'普宁红领巾实验学校老师性侵学生',
        'event_time':'2019-07-06',
        'post_items':[
            'https://wx1.sinaimg.cn/mw690/006tRbCygy1g4q0tns8prj30gg0zkq62.jpg',
            'https://wx3.sinaimg.cn/mw690/006tRbCygy1g4q0ridqw8j30k80la41d.jpg',
            'https://wx4.sinaimg.cn/mw690/006tRbCygy1g4q0to6qy6j30k00zkjuu.jpg',
            'https://wx1.sinaimg.cn/mw690/006tRbCygy1g4q0tomgdbj30k00zkdjo.jpg',
            'https://wx1.sinaimg.cn/mw690/006tRbCygy1g4q0tp24i4j30k00zkjw2.jpg',
            'https://wx1.sinaimg.cn/mw690/006tRbCygy1g4q0tn4it9j30k00zk0w6.jpg',
            'https://wx4.sinaimg.cn/mw690/006tRbCygy1g4pizxevl5j30lq0m6770.jpg',
            'https://wx1.sinaimg.cn/mw690/006tRbCygy1g4pizx64e7j30m70j00v5.jpg',
            'https://wx1.sinaimg.cn/mw690/006tRbCygy1g4pizx17pgj30ci0m8gmn.jpg',
            'https://wx4.sinaimg.cn/mw690/006tRbCygy1g4pizwwl15j30a80m7gmy.jpg',
        ]#
    }
    commitment(content,token)


def commitment(data,token):
    headers = {
        'content-type': 'application/json'
    }
    r = requests.post('http://'+config['server_host']+'/REQ_UPLOAD?token='+token,data=json.dumps(data),headers=headers)
    return_data = json.loads(r.content)

    if return_data['status'] != 0:
        print(str(return_data['msg']))
        # return
    else:
        print(return_data['data'])
        # return return_data['data']


upload()

