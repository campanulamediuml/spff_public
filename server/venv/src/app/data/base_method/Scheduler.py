import time
import heapq
from threading import Timer
import random

TIME_ACCURACY = 1  # 时间精度，时间精度不是越小越好！你的Task每次循环超过了这个值,将影响准确度


class Scheduler(object):
    tasks = []

    @staticmethod
    def add(task):
        heapq.heappush(Scheduler.tasks, (task.get_runtime(), task))

    @staticmethod
    def run(is_timer = False):
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
        return self._runtime + random.random()/100

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
        self.start(self)
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
class IntervalTask(Task):

    def __init__(self, interval, func, args=()):
        Task.__init__(self, func, args)
        self._interval = interval
        self._cycle = True
        self.start()


# def test(x, y):
#     print(time.time())

#     print(x + y)



# if "__main__" == __name__:
#     Scheduler.run()
#     now = time.time()

#     CountdownTask(2, test, (1, 2))

#     print("end")