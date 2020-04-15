from config.db_config import db_config
from data.dbserver.data_manager import data_manager

class Data(object):
    Base = data_manager(db_config)

    @staticmethod
    def new():
        id = Data.Base.new()
        return id

    @staticmethod
    def create(table, colums):
        return Data.Base.create(table, colums)

    @staticmethod
    def insert(table, params, is_commit=True):
        return Data.Base.insert(table, params, is_commit)

    @staticmethod
    def find(table, conditions, fields='*', order=None):
        return Data.Base.find(table, conditions, fields, order)

    @staticmethod
    def select(table, conditions, fields='*', order=None):
        return Data.Base.select(table, conditions, fields, order)

    @staticmethod
    def update(table, conditions, params, is_commit=True):
        return Data.Base.update(table, conditions, params, is_commit)

    @staticmethod
    def delete(table, conditions, is_commit=True):
        return  Data.Base.delete(table, conditions, is_commit)

    @staticmethod
    def find_last(table, conditions, info, limit):
        return Data.Base.find_last(table, conditions, info, limit)

    @staticmethod
    def query(sql):
        return Data.Base.query(sql)

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
            'busy_base': {
                'count': len(busy_list),
                'lists': busy_list,
                'executing': sql_executing,
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





