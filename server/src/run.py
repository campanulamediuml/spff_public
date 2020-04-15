import os
import time
import sys
from common.common import common_tools

doc = """Error - 指令缺失
命令提示:
check  查看运行进程
kill 关闭进程
restart 启动进程
start 启动进程
"""
script_list = ['http_main','weibo_bot']



def start():
    if len(sys.argv) < 3:
        print('缺少脚本名称')
        return


    script = sys.argv[2]
    if script == 'http_main':
        name = script+ common_tools.time_to_str(int(time.time())).replace(' ', '-')+'.log'
        query = 'cp '+script+'.log'+' '+name
        os.system(query)
        print('上一份日志备份到',name)
        time.sleep(1)

        query = 'nohup python3 -u '+script+'.py > '+script+'.log 2>&1 &'
        os.system(query)
        print('运行'+script+'.py成功, 日志位置>> '+script+'.log')

    elif script == 'weibo_bot':
        name = script + common_tools.time_to_str(int(time.time())).replace(' ', '-') + '.log'
        query = 'cp ' + script + '.log' + ' ' + name
        os.system(query)
        print('上一份日志备份到', name)
        time.sleep(1)

        query = 'nohup python3 -u ' + script + '.py '+sys.argv[3]+' > ' + script + '.log 2>&1 &'
        os.system(query)
        print('运行' + script + '.py成功, 日志位置>> ' + script + '.log')


    else:
        print('非法指令')

    print('start done!')
    open_log = 'cat '+script+'.log'
    time.sleep(0.5)
    os.system(open_log)
    return
    # except Exception as e:
    #     print('缺少脚本名称')
    #     return

def check():
    query = 'ps -x | grep python3'
    os.system(query)
    return

def kill():
    # print('长度为',len(sys.argv))
    if len(sys.argv) < 3:
        print('缺少脚本名称')
        return

    script = sys.argv[2]
    if script not in script_list:
        return print('这个进程无法通过运维脚本杀死...')

    query = 'ps -x | grep python3'
    running_proc = os.popen(query).readlines()
    for line in running_proc:
        # print(line)
        line_info = line.split()
        # print(line_info)
        if len(line_info) > 6:
            if script in line_info[6]:
                pid = line.split()[0]
                # print(pid)
                query = 'kill '+str(pid)
                os.system(query)
                print('杀死',script,pid,'完毕')
    return

def execute_command(command):


    if command == 'start':
        start()
        return

    if command == 'kill':
        kill()
        return

    if command == 'restart':
        print('restarting...')
        kill()
        start()
        print('restart_done!')
        return

    if command == 'check':
        check()
        return


def main():
    if len(sys.argv) == 1:
        print(doc)
        return
    command = sys.argv[1]
    if command not in ['clean','start','restart','check','kill']:
        print('command error!')
        return
    else:
        execute_command(command)


main()
