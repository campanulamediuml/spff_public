import time

def str_to_time(time_str):
    timeArray = time.strptime(str(time_str), "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(timeArray))
    return time_stamp

tmp = []
while 1:
	date = input('输入日期(YYYY-MM-DD)')
	tmp.append(date)

