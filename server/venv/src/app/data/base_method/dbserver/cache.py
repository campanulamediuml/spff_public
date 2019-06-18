from app.data.server import Data
from app.data.base_method.Scheduler import IntervalTask
from config import refresh_time
import time
import json

def time_to_str(times):
    date_array = datetime.datetime.utcfromtimestamp(times+(8*3600))
    return date_array.strftime("%Y-%m-%d %H:%M:%S")


def bigger(line,conditions):
    if line[conditions[0]] > conditions[2]:
        return True
    else:
        return False

def small(line,conditions):
    if line[conditions[0]] < conditions[2]:
        return True
    else:
        return False

def equal(line,conditions):
    if line[conditions[0]] == conditions[2]:
        return True
    else:
        return False

def not_eqal(line,conditions):
    if line[conditions[0]] != conditions[2]:
        return True
    else:
        return False

def big_equal(line,conditions):
    if line[conditions[0]] >= conditions[2]:
        return True
    else:
        return False

def small_equal(line,conditions):
    if line[conditions[0]] <= conditions[2]:
        return True
    else:
        return False


def judge(line,conditions):
    res = False
    for cond in conditions:
        if judge_dict[cond[1]](line,cond) == True:
            res = True
    
    if res == True:
        return True
    else:
        return False
    # 判断条件是否成立


def get_all_data():
    start_time = time.time()

    table_list = Data.get_tables()
    data_strct = {}
    for table in table_list:
        ctime = time.time()
        print('reading',table,'...')
        data_strct[table] = Data.select(table,[])
        print('read',table,'done! spend',time.time()-ctime,'seconds')

    print('read database done!')
    print('spend',time.time()-start_time,'seconds')

    return data_strct
    # 读取整个数据库

judge_dict = {
            '=':equal,
            '!=':not_eqal,
            '>':bigger,
            '<':small,
            '>=':big_equal,
            '<=':small_equal,  
        }
# 判断字典
                

class cached_base(object):
    def __init__(self):  
        self.data_all = {}

        IntervalTask(1, self.refresh_db)

    # 获取所有数据类型
    def refresh_db(self):

        time_now = time_to_str(int(time.time())).split()[1].split(':')[:2]
        if ':'.join(time_now) == refresh_time:
            for table in self.data_all:
                Data.delete(table,[])
                Data.insert(table,self.data_all[table])
            time.sleep(60)
        else:
            pass
        return

    def get_base(self):
        return get_all_data()
        # 提取整个数据库

    def get_cached_base(self):
        return self.data_all

    def get_table_names(self):
        result = []
        for table in self.data_all:
            result.append(table)

        return result

        # 获取表格名称
    def refresh_one_table(self,table):
        # self.data_all.pop(table)
        print('importing..',table)
        self.data_all[table] = Data.select(table,[])
        print('importing..',table,'done!')
        return

    def append_lines(self,table):
        last_id = self.data_all[table][-1]['id']
        res = Data.select(table,[('id','>',last_id)])
        if res != None:
            if len(res) != 0:
                self.data_all[table] = self.data_all[table]+res
        return 
        # 添加新的行

    def cache_dumps(self):
        content = json.dumps(self.data_all)
        open('base_dump.dumps','w').write(content)
        return
        # 缓存成json

    def find(self,table,conditions):
        if table not in self.data_all:
            self.refresh_one_table(table)

        table_content = self.data_all[table]
        
        for line in table_content:
            if judge(line,conditions) == True:
                return line
        return {}
        # 查询

    def select(self,table,conditions):
        if table not in self.data_all:
            self.refresh_one_table(table)

        table_content = self.data_all[table]
        
        result = []
        if conditions == []:
            return table_content

        for line in table_content:
            if judge(line,conditions) == True:
                result.append(line)

        return result
        # 查询多条

    def insert(self,table,content):
        Data.insert(table,content)
        if table in self.data_all:
            self.append_lines(table)
        else:
            self.refresh_one_table(table)

        return

    def update(self,table,conditions,params):
        if table in self.data_all:
            table_content = self.data_all[table]

            table_id_list = []
            tmp = []
            if conditions == []:
                for line in table_content:
                    table_id_list.append(line['id'])
                    tmp.append(line)

            else:
                for line in table_content:
                    if judge(line,conditions) == True:
                        table_id_list.append(line['id'])
                        tmp.append(line)

            Data.update(table,conditions,params)

            for line in tmp:
                self.data_all[table].remove(line)

            for i in table_id_list:
                res = Data.find(table,[('id','=',i)])
                for line in table_content:
                    if line['id'] > res['id']:
                        line_index = table_content.index(line)
                        if line_index == 0:
                            tail = [res]+table_content
                        else:
                            tail = table_content[:line_index] + [res] + table_content[line_index:]
                        break
                table_content = tail

            self.data_all[table] = table_content


        else:
            Data.update(table,conditions,params)
            self.data_all[table] = Data.select(table,[])

        return

    def delete(self,table,conditions):
        if table in self.data_all:
            table_content = self.data_all[table]

            del_line = []

            for line in table_content:
                if judge(line,conditions) == True:
                    del_line.append(line)

            for i in del_line:
                table_content.remove(i)

            Data.delete(table,conditions)

        else:
            Data.delete(table,conditions)
            self.data_all[table] = Data.select(table,[])

        return

    def truncate(self,table):
        if table in self.data_all:
            self.data_all[table] = []

        else:
            self.data_all[table] = []

        Data.truncate(table)

        return









            




            
        
