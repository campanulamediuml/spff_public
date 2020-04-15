import time

from data.dbserver.base import Base
# from config.config import db_config
from common.common import common_tools
from common.Scheduler import IntervalTask

class data_manager(object):
    def __init__(self,db_config):
        self.t_data = db_config
        self.sql_pool = {}

        sql = self._create_new_sql()
        self.add_new_sql(sql)
        print('创建首批数据库链接实例')
        IntervalTask(10,self.keep_connect)

    # def kill_hanged_connection(self):
    #     dead_sql = []
    #

    def keep_connect(self):
        can_update_sql = []
        for sql in self.sql_pool.values():
            if int(time.time())-sql.get_last_connect_time()  > 30:
                can_update_sql.append(sql)

        for sql in can_update_sql:
            if sql.is_busy() == False:
                sql.become_busy()
                sql.keep_connect()
                sql.become_free()
        return

    def find_free_sql(self):
        for sql in self.sql_pool.values():
            if sql.is_busy() == False:
                sql.become_busy()
                return sql
        print('数据库连接池全忙状态，创建新的数据库链接')
        sql = self._create_new_sql()
        sql.become_busy()
        self.add_new_sql(sql)
        print('创建完毕')
        common_tools.dbg_db('数据库连接池全忙状态，创建新的数据库链接', '新连接id:', id(sql))
        return sql

    def add_new_sql(self,sql):
        self.sql_pool[id(sql)] = sql
        return


    def _create_new_sql(self):
        sql = Base(self.t_data['host'], self.t_data['user'], self.t_data['password'], self.t_data['database'])
        # sql.become_busy()
        # self.sql_pool.append(sql)
        return sql

    def new(self):
        sql = Base(self.t_data['host'], self.t_data['user'], self.t_data['password'], self.t_data['database'])
        self.sql_pool[id(sql)] = sql
        return id(sql)

    def get_tables(self):
        sql = self.find_free_sql()
        # sql.become_busy()
        print('执行这次sql请求的链接是', id(sql))
        result = sql._tables
        sql.become_free()
        return result


    def create(self,table, colums):
        sql = self.find_free_sql()
        # sql.become_busy()
        print('执行这次sql请求的链接是', id(sql))
        result = sql.create(table, colums)
        sql.become_free()
        return result


    def insert(self,table, params, is_commit=True):
        sql = self.find_free_sql()
        # sql.become_busy()
        # print('执行这次sql请求的链接是', id(sql))
        result = sql.insert(table, params, is_commit)
        sql.become_free()
        return result


    def find(self,table, conditions, fields='*', order=None):
        sql = self.find_free_sql()
        # sql.become_busy()
        # print('执行这次sql请求的链接是', id(sql))
        result = sql.find(table, conditions, fields, order)
        sql.become_free()
        return result


    def select(self,table, conditions, fields='*', order=None):
        sql = self.find_free_sql()
        # sql.become_busy()
        # print('执行这次sql请求的链接是', id(sql))
        result = sql.select(table, conditions, fields, order)
        sql.become_free()
        return result


    def update(self,table, conditions, params, is_commit=True):
        sql = self.find_free_sql()
        # sql.become_busy()
        # print('执行这次sql请求的链接是', id(sql))
        result = sql.update(table, conditions, params, is_commit)
        sql.become_free()
        return result


    def delete(self,table, conditions, is_commit=True):
        sql = self.find_free_sql()
        # sql.become_busy()
        # print('执行这次sql请求的链接是', id(sql))
        result = sql.delete(table, conditions, is_commit)
        sql.become_free()
        return result


    def find_last(self,table, conditions, info, limit):
        sql = self.find_free_sql()
        # sql.become_busy()
        # print('执行这次sql请求的链接是', id(sql))
        result = sql.find_last(table, conditions, info, limit)
        sql.become_free()
        return result



    def query(self,sql_query):
        sql = self.find_free_sql()
        print('执行这次sql请求的链接是', id(sql))
        result = sql.query(sql_query)
        sql.become_free()
        return result


