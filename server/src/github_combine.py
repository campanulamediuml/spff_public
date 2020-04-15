import os
import time

from simulator import simulator
from common.common import common_tools

name = ''
pw = ''

def get_file_path():
    running_path = os.path.abspath('.')
    path = running_path.split('/')
    client_path = path[:-2]
    client_path.append('source/')
    client_path = '/'.join(client_path)
    return client_path

def get_file_index():
    path = get_file_path()
    res = os.popen('ls '+path).readlines()
    return res

def upload_files():
    sm = simulator()
    sm.admin_login(name,pw)
    file_index = get_file_index()
    pass_filename = ['README.md','_config.yml']
    for file_name in file_index:
        file_name = file_name.strip()
        if file_name not in pass_filename:
            file_content = open(get_file_path()+file_name.strip(),'r').read()
            data = {
                'title':file_name,
                'content':file_content,
                'event_time': common_tools.time_to_str(int(time.time())).split()[0],
                'post_items':[]
            }
            res = sm.upload(data)
            print(res)



if __name__=='__main__':
    upload_files()
    # data = create_upload_data()
    # res = sm.upload(data)