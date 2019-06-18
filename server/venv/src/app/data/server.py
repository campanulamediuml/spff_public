from app.data.base_method.dbserver.base import Base
from config import SERVER


class Data(object):
    t_data = SERVER['DATA_BASE']
    sql = Base(t_data['host'], t_data['user'], t_data['password'], t_data['database'])

    @staticmethod
    def get_tables():
        return Data.sql._tables

    @staticmethod
    def insert(table, params, is_commit = True):
        return Data.sql.insert(table, params, is_commit)

    @staticmethod
    def find(table, conditions, fields = '*'):
        return Data.sql.find(table, conditions, fields)

    @staticmethod
    def select(table, conditions, fields='*',order=None, choose='and'):
        return Data.sql.select(table, conditions, fields,order)

    @staticmethod
    def update(table, conditions, params, is_commit = True):
        return Data.sql.update(table, conditions, params, is_commit)

    @staticmethod
    def delete(table, conditions, is_commit = True):
        return Data.sql.delete(table, conditions, is_commit)

    @staticmethod
    def get_max_field(table , field='id'):
        sql = "select max(%s) from %s"%(field, table)
        result = Data.query(sql)
        if result[0][0] is None:
            return 1

        return result[0][0]

    @staticmethod
    def query(sql):
        # print(sql)
        return Data.sql.query(sql)

    @staticmethod
    def truncate(table):
        # print(sql)
        return Data.sql.truncate(table)

