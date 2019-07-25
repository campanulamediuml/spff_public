from app.data.server import Data
from app.common import common
import time
import json


# params = {
#     'nickname':json.dumps('campanula').replace('\\','\\\\')
# }

# Data.update('user',[('id','=',2)],params)



def write_main_info():
    title = '南昌红谷滩杀人'

    content = '''32岁南昌男子从背后袭击，当街将24岁女子捅杀】24日下午5时18分许，南昌市红谷滩发生一起杀人案。27日记者从南昌公安局了解到，犯罪嫌疑人万某弟(男，32岁，南昌人)已被控制，作案动机仍在调查。监控视频显示，行凶者当时冲向并排行走的三人，持刀向其中一名女子砍去。女子倒地后，行凶者仍不依不饶。另据@北京时间 报道，凶手曾想杀“个子高”女子，后发现另一女子“更白更漂亮”。'''

    content = json.dumps(content)#.replace('\\','\\\\')
    content_md5 = common.get_md5(content)

    event_time = '2019-05-28 00:00:00'
    event_time = common.str_to_time(event_time)

    params = {
            'user_id':2,
            'ctime':int(time.time()),
            'content':content,
            'content_md5':content_md5,
            'event_time':event_time,
            'title':title
        }
    # Data.update('case_info',[('content_md5','=',content_md5)],params)
    Data.insert('case_info',params)


def update_post_items():
    res = Data.select('case_post_item',[('id','!=',0)])
    for line in res:
        Data.update('case_post_item',[('id','=',line['id'])],{'raw_url':line['post_item']})
    return

# update_post_items()