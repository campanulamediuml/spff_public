import base64
import datetime
import string
import time
import hashlib

import requests
from gevent import getcurrent
from math import radians, sin, cos, asin, sqrt
import random
import sys

import json

rand_string = 'qwertyuiopasdfghjklzxcvbnm1234567890'

class common_tools(object):
    session = requests.Session()

    @staticmethod
    def time_to_str(times=time.time()):
        date_array = datetime.datetime.utcfromtimestamp(times + (8 * 3600))
        return date_array.strftime("%Y-%m-%d %H:%M:%S")
        # 时间戳转换时间

    @staticmethod
    def str_to_time(time_str):
        timeArray = time.strptime(str(time_str), "%Y-%m-%d %H:%M:%S")
        time_stamp = int(time.mktime(timeArray))
        return time_stamp
        # 相反

    @staticmethod
    def create_rand_string(length):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

    @staticmethod
    def sorted_dct_to_string(dct,need_lower=False):
        if need_lower == True:
            return '&'.join(['%s=%s' % (key.lower(), dct[key]) for key in sorted(dct)])
        else:
            return '&'.join(['%s=%s' % (key, dct[key]) for key in sorted(dct)])


    @staticmethod
    def get_md5(string):
        md5 = hashlib.md5(string.encode(encoding='UTF-8')).hexdigest()
        return md5
        # 计算字符串md5

    @staticmethod
    def get_sha1(string):
        md5 = hashlib.sha1(string.encode(encoding='UTF-8')).hexdigest()
        return md5
        # 计算字符串md5

    @staticmethod
    def get_file_md5(binary):
        md5 = hashlib.md5(binary).hexdigest()
        return md5
        # 文件md5计算
    @staticmethod
    def get_base64(binary):
        res = base64.b64encode(binary)
        return res.decode('utf-8')

    @staticmethod
    def decode_base64(data):
        res = base64.b64decode(data)
        return res.decode('utf-8')

    @staticmethod
    def get_event_id():
        id_string = str(id(getcurrent()))
        return common_tools.get_md5(id_string)
        # 获得当前进程id编码


    # 计算两点之间的距离,LBS 球面距离公式
    @staticmethod
    def haversine(lon1, lat1, lon2, lat2):
        # 经度1，纬度1，经度2，纬度2 （十进制度数）GPS距离计算
        # 将十进制度数转化为弧度
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine公式
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        dis = 2 * asin(sqrt(a)) * 6371 * 1000  # 地球平均半径，单位为公里
        dis = int(dis)
        return dis
        # 返回单位为米

    @staticmethod
    def dict_to_xml(data):
        xml = ''
        for key, value in data.items():
            xml += '<{0}>{1}</{0}>'.format(str(key), str(value))
        xml = '<xml>{0}</xml>'.format(xml)
        return xml

    @staticmethod
    def dict_to_url_params(data):
        argStr = ''
        for p, v in data.items():
            argStr = argStr + p + '=' + str(v) + '&'
        argStr = argStr[:-1]
        return argStr


    @staticmethod
    def dbg_db(*args):
        res = '[' + common_tools.time_to_str(int(time.time())) + ']----------process:' + str(sys.argv[-1]) + '\n'
        info = ''
        for i in args:
            info += '    '
            info += str(i)
            info += '\n'
        debug_info = res + info
        open('db.log', 'a').write(debug_info)
        return
        # print(*args)

    @staticmethod
    def post(url, payload=None, params=None,headers = None,show_headers=True,show_data=True):
        if headers is not None:
            headers['Content-Type'] = 'application/json'
        # try:
        r = common_tools.session.post(url, params=params, json=payload, headers=headers)
        # except:
        #     return
        if show_data == True:
            print('<===========POST===========>')
            print('<===========', url, '===========>')
            print('<===========', payload, '===========>')
            print(r,r.text)
            print('\n')
        if show_headers == True:
            for name in r.headers:
                print(name, r.headers[name])
        if r.status_code == requests.codes.ok:
            return (r.text)
        else:
            return

    @staticmethod
    def get(url, params=None,headers =None, show_headers=True,show_data=True):
        if headers is not None:
            headers['Content-Type'] = 'application/json'
        try:
            r = common_tools.session.get(url, params=params, headers=headers)
        except:
            return
        if show_data == True:
            print('<===========GET===========>')
            print('<===========', url, '===========>')
            print(r, r.text)
            print('\n')
        if show_headers == True:
            for name in r.headers:
                print(name,r.headers[name])
        if r.status_code == requests.codes.ok:
            return (r.text)
        else:
            return


if __name__=='__main__':
    res = common_tools.get_base64('测试'.encode('utf-8'))
    print(res)
    res = common_tools.decode_base64(res)
    print(res)

