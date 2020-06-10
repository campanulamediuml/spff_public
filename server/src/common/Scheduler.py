import threading
import time
import heapq
from threading import Timer
import random
# import _thread as thread

TIME_ACCURACY = 1  # 时间精度，时间精度不是越小越好！你的Task每次循环超过了这个值,将影响准确度

# def

def IntervalTask(sec,func,args=(),immediatly=True,thread_name = ''):
    def run(*args):
        if immediatly is False:
            time.sleep(sec)
        while 1:

            func(*args)
            time.sleep(sec)
    t = threading.Thread(target=run, args=args)
    if thread_name != '':
        t.name = thread_name
    t.start()
    # t.join()

def normal_task(sec,func,args=(),thread_name=''):
    def run(*args):
        time.sleep(sec)
        func(*args)
    t = threading.Thread(target=run, args=args)
    if thread_name != '':
        t.name = thread_name
    t.start()
    # t.join()
    # threading.enumerate()
    # print(threading.enumerate())


class Scheduler(object):
    tasks = []

    @staticmethod
    def add(task):
        heapq.heappush(Scheduler.tasks, (task.get_runtime(), task))

    @staticmethod
    def run(is_timer=False):
        now_time = time.time()
        while Scheduler.tasks and now_time >= Scheduler.tasks[0][0]:
            _, task = heapq.heappop(Scheduler.tasks)
            task.call()

            if task.is_cycle():
                task.up_runtime()
                Scheduler.add(task)

        if is_timer is True:
            t = Timer(TIME_ACCURACY, Scheduler.run, args=[True])
            t.start()


'''
定时任务
func:要定时执行的方法
args:函数的参数（tuple）
执行start()此定时器生效
'''


class Task(object):
    def __init__(self, func, args=()):
        self._func = func
        self._args = args
        self._runtime = time.time()
        self._interval = 0
        self._cycle = False

    def __lt__(self, other):
        return False

    def call(self):
        self._func(*self._args)

    def up_runtime(self):
        self._runtime += self._interval

    def is_cycle(self):
        return self._cycle

    def get_runtime(self):
        return self._runtime + random.random() / 100

    def start(self):
        Scheduler.add(self)


'''
作用：简单定时任务
runtime:开始时间(时间戳)
'''


class NormalTask(Task):

    def __init__(self, runtime, func, args=()):
        Task.__init__(self, func, args)
        self._runtime = runtime
        self.start()


'''
作用：倒计时定时任务
countdown:倒计时，这个时间后开始执行（单位：秒）
'''


class CountdownTask(Task):

    def __init__(self, countdown, func, args=()):
        Task.__init__(self, func, args)
        self._runtime += countdown
        self.start()


'''
作用：循环定时任务
interval:循环周期（单位：秒）
'''


# 使用方法：
'''
res = []
for i in data:
    r = func(data)
    res.append(data)
return res
=======顺序执行======

res = super_charger(func,data)
#####增压器#######
=======加速执行======
# '''
class func_engine(threading.Thread):
    def __init__(self,func,args=()):
        super(func_engine,self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None
    # 并发优化
def turbo(func,arg_list):
    # global func_runner
    # 函数增压器！
    li = []
    for i in arg_list:
        runner = func_engine(func, args = i)
        li.append(runner)
        runner.start()

    result = []
    for i in li:
        i.join()
        result.append(i.get_result())
    return result

# ↓最终加速工具，请调用这个函数
def super_charger(func,arg_list):
    return turbo(func,arg_list)
# ↑最终加速工具，请调用这个函数



if "__main__" == __name__:
    # res = [(1,2,3),(4,5,6),(7,8,9)]
    # print(turbo(foo,res))
    pass
