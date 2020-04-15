thread_num = 8
# 服务器线程数量
debug_mode = False
# 是否debug
update_token = False
# 是否开启更新token
thread_pool_num = 40
# 线程池数量
show_sql = False
# 是否打印sql语句
logging_data_length = 1024
# post收到的数据大于这个值的话不显示

logical_url = 'http://127.0.0.1'

tel_verify = {
    'url': 'http://m.5c.com.cn/api/send/index.php',
    'api_key': '',
    'username': '',
    'pw': '',
}

http_config = {
    'host': '0.0.0.0',
    'port': 9999
}

file_url='http://127.0.0.1/'
file_path='client/web_index/post_items/'
file_name=['jpg','jpeg','gif']
# ws超时时间
ws_time_out = 15
# token超时时间
token_time_out = 60 * 10
