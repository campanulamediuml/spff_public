from common.Scheduler import IntervalTask, normal_task
from config.db_config import db_config
from data.cache.cache import Cache
from data.dbserver.data_manager import data_manager

class Data(object):
    cache_timer = 30
    Base = data_manager(db_config)

    @staticmethod
    def cache_init(table=None):
        # 数据缓存
        if table is not None:
            Data.update_cache(table)
            return
        print('开始数据缓存')
        table_list = Data.query('show tables')
        for i in table_list:
            table_name = i[0]
            Data.update_cache(table_name)
        print('数据缓存完毕')
        IntervalTask(Data.cache_timer, Data.update_all_cache, immediatly=False, thread_name='Data_cache_interval')

    @staticmethod
    def update_all_cache():
        print('周期刷新缓存开始')
        table_list = Data.query('show tables')
        for i in table_list:
            table_name = i[0]
            normal_task(0, Data.update_cache, (table_name,))
            # Data.update_cache(table_name)
        print('周期刷新缓存完毕')
        

    @staticmethod
    def check_connections():
        sql_pool = Data.Base.sql_pool
        busy_list = []
        all_list = []
        free_list = []
        sql_executing = {}
        for sql_id in sql_pool:
            sql = sql_pool[sql_id]
            if sql.is_busy() == True:
                busy_list.append(sql_id)
                sql_executing[sql_id] = sql.executing_query

            if sql.is_busy() == False:
                free_list.append(sql_id)
            all_list.append(sql_id)

        result = {
            'busy_base':{
                'count':len(busy_list),
                'lists':busy_list,
                'executing':sql_executing,
            },
            'free_base': {
                'count': len(free_list),
                'lists': free_list
            },
            'all_base': {
                'count': len(all_list),
                'lists': all_list
            }
        }
        return result


    @staticmethod
    def create(table, colums):
        return Data.Base.create(table, colums)

    @staticmethod
    def insert(table, params, is_commit=True):
        res = Data.Base.insert(table, params, is_commit)
        print('触发缓存', table)
        normal_task(0, Data.update_cache, (table,))
        return res

    @staticmethod
    def find(table, conditions, fields=('*',), order=None):
        return Data.Base.find(table, conditions, fields, order)

    @staticmethod
    def select(table, conditions,fields=('*',), order=None):
        return Data.Base.select(table, conditions, fields, order)

    @staticmethod
    def update(table, conditions, params, is_commit=True):
        data = Data.Base.update(table, conditions, params, is_commit)
        print('触发缓存', table)
        normal_task(0, Data.update_cache, (table,))
        return data

    @staticmethod
    def delete(table, conditions, is_commit=True):
        res = Data.Base.delete(table, conditions, is_commit)
        print('触发缓存', table)
        normal_task(0, Data.update_cache, (table,))
        return res

    @staticmethod
    def find_last(table, conditions, info, limit):
        return Data.Base.find_last(table, conditions, info, limit)

    @staticmethod
    def query(sql):
        return Data.Base.query(sql)

    @staticmethod
    def update_cache(table):
        data = Data.select(table, [])
        # print(data)
        Cache.update_table(table, data)
        return

    @staticmethod
    def get_cache(table, safe=False):
        # print('取得缓存')
        data = Cache.get_table(table, safe)
        if data is None:
            data = {}
            print('缓存未命中')
            print(table)
            tmp = Data.select(table, [])
            for line in tmp:
                if 'id' in line:
                    data[line['id']] = line
            normal_task(0, Data.update_cache, (table,))
        return data

    @staticmethod
    def get_table_list():
        table_name_list = []
        for table in Cache.table_index:
            table_name_list.append(table)

        return table_name_list




