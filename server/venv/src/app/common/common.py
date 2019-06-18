import datetime
import time
import config
import hashlib
import json
from app.data.server import Data



# 时间戳转2018-01-01 8:00:00
def time_to_str(times):
    date_array = datetime.datetime.utcfromtimestamp(times+(8*3600))
    return date_array.strftime("%Y-%m-%d %H:%M:%S")


# 获取md5
def get_md5(string):
    md5 = hashlib.md5(string.encode('utf-8')).hexdigest()
    return md5


# 时间转unix时间戳
def str_to_time(time_str):
    timeArray = time.strptime(str(time_str), "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(timeArray))
    return time_stamp
