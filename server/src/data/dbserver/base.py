import pymysql
# from common.Scheduler import IntervalTask
import time
import datetime
import sys

from common.common import common_tools
from config import config


class base(object):

    def __init__(self, host, user, psw, dbname):
        self._host = host
        self._user = user
        self._psw = psw
        self._dbname = dbname
        self._tables = {}
        self._is_busy = 0
        self.init_time = int(time.time())
        self.executing_query = ''
        self.last_execute_time = int(time.time())
        self.db = None
        self.connect_db()
        self.last_connect_time = int(time.time())

    def connect_db(self):
        try:
            self.db = pymysql.connect(self._host, self._user, self._psw, self._dbname, charset='utf8', autocommit=True)
            self._load_tables()
            print('数据库模块连接成功')
            common_tools.dbg_db('数据库模块连接成功')
            # IntervalTask(30, self.keep_connect)
        except Exception as e:
            print(e)
            print('数据库没有成功链接')
            common_tools.dbg_db('数据库模块连接成功', str(e))
            pass

    def become_busy(self):
        self._is_busy = 1
        return

    def become_free(self):
        self._is_busy = 0
        return

    def is_busy(self):
        if self._is_busy == 1:
            return True
        else:
            return False

    def keep_connect(self):
        if self.db == None:
            self.connect_db()

        # print(id(self),'进行连接')
        self.query('select 1')
        # print('数据库心跳')

    def connect(self):
        self.db = pymysql.connect(self._host, self._user, self._psw, self._dbname, charset='utf8')

    def load_an_table(self, table):
        sql = 'show fields from ' + table
        res = self.query(sql)
        self._tables[table] = list(map(lambda x: x[0], res))
        return

    # 加载所有数据库表名
    def _load_tables(self):
        sql = 'show tables'
        res = self.query(sql)
        tables = tuple(map(lambda x: x[0], res))
        # print(tables)
        for table in tables:
            sql = 'show fields from ' + table
            # 
            res = self.query(sql)
            self._tables[table] = list(map(lambda x: x[0], res))

    def _load_all_fileds(self):
        pass

    def create(self, table, colums):
        sql = 'create table %s(' % table

        tail = ''
        for item in colums:
            col = ''
            for i in item:
                col += str(i)
                col += ' '
            col += ','
            tail += col

        tail = tail[:-1] + ')'
        sql += tail

        # 

        self.query(sql)
        self.db.commit()
        return

    def find_info(self, table, conditions, fields, order):
        sql = 'select %s from %s where  ' % (','.join(fields), table)
        # if conditions == []:
        for unit in conditions:
            value = unit[2]
            if type("") == type(value):
                value = "'%s'" % value

            sql = sql + "%s %s %s " % (unit[0], unit[1], value) + "  and "

        if 0 < len(conditions):
            sql = sql[0: -4]
        else:
            sql = sql[:-7]

        if order is not None:
            sql += 'order by %s %s ' % (order[0], order[1])
        return sql

    # 查找数据（单条）
    def find(self, table, conditions, fields=('*',), order=None):
        sql = self.find_info(table, conditions, fields, order)

        sql += " limit 1"

        # 
        res = self.query(sql)
        if res is None:
            return None

        if 0 == len(res):
            return None

        if table not in self._tables:
            self.load_an_table(table)

        if fields[0] == '*' and len(fields) == 1:
            fieldList = self._tables[table]

        else:
            fieldList = fields

        self.db.commit()
        return dict(zip(fieldList, res[0]))

    # 查找数据
    def select(self, table, conditions, fields=('*',), order=None):
        sql = self.find_info(table, conditions, fields, order)

        # 
        res = self.query(sql)
        if res is None:
            return None

        if 0 == len(res):
            return None

        if table not in self._tables:
            self.load_an_table(table)

        if fields[0] == '*' and len(fields) == 1:
            fieldList = self._tables[table]
        else:
            fieldList = fields

        result = []
        for data in res:
            data = dict(zip(fieldList, data))
            result.append(data)

        self.db.commit()
        return result

    def insert(self, table, content, isCommit=True):
        if type(content) == type([]):
            sql = ''
            for params in content:
                keys = str(tuple(params.keys()))
                keys = keys.replace("'", "")
                values = str(tuple(params.values()))
                if (1 == len(params)):
                    keys = keys[:-2] + ")"
                    values = values[:-2] + ")"

                sql += 'insert into %s%s values %s ;' % (table, keys, values)
            # 
            self.query(sql)
            if True == isCommit:
                self.db.commit()
        else:
            params = content
            keys = str(tuple(params.keys()))
            keys = keys.replace("'", "")
            values = str(tuple(params.values()))
            if (1 == len(params)):
                keys = keys[:-2] + ")"
                values = values[:-2] + ")"

            sql = 'insert into %s%s values %s ;' % (table, keys, values)
            # 
            self.query(sql)
            if True == isCommit:
                self.db.commit()

        return

    def update(self, table, conditions, params, isCommit=True):
        sql = 'update %s set ' % table
        for param, value in params.items():
            if type("") == type(value):
                value = "'%s'" % value
            sql = sql + " %s = %s," % (param, value)

        sql = sql[:-1]
        if len(conditions) > 0:
            sql += " where "

        for unit in conditions:
            value = unit[2]
            if type("") == type(value):
                value = "'%s'" % value

            sql = sql + "%s %s %s " % (unit[0], unit[1], value) + " and "

        if 0 < len(conditions):
            sql = sql[0: -4]

        # 
        self.query(sql)
        if True == isCommit:
            self.db.commit()

        return

    def delete(self, table, condition, is_commit):
        sql = 'delete from %s where ' % table
        for unit in condition:
            value = unit[2]
            if type("") == type(value):
                value = "'%s'" % value

            sql = sql + "%s %s %s " % (unit[0], unit[1], value) + " and "

        if 0 < len(condition):
            sql = sql[0: -4]
        else:
            sql = sql[:-7]
        # 
        # 
        self.query(sql)
        if is_commit is True:
            self.db.commit()

        return

    def query(self, sql):

        self.executing_query = sql

        if sql != 'select 1':
            if config.show_sql == True:
                print(sql)
        try:
            self.db.ping(reconnect=True)
        except Exception as e:
            print(sql, '数据库连接出错', str(e), '进行重连')
            common_tools.dbg_db(sql, '数据库连接出错', str(e), '进行重连')
            self.connect()
        cursor = self.db.cursor()
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            self.update_last_execute_time()
            self.db.commit()
            # common_tools.dbg_db(sql,'数据库查询成功')
        except Exception as e:
            print('<--------DBERROR-------->')
            print(sql)
            print('数据库查询出错', str(e))
            print('<--------DBERROR-------->')
            common_tools.dbg_db(sql, '数据库查询出错', str(e))
            results = None

        self.update_last_connect_time()

        self.executing_query = ''

        return results
        # results = cursor.fetchall()

    def update_last_connect_time(self):
        self.last_connect_time = int(time.time())
        return

    def update_last_execute_time(self):
        self.last_execute_time = int(time.time())
        return

    def get_last_connect_time(self):
        return self.last_connect_time

    def query_one(self, sql):
        self.db.ping(reconnect=True)
        # cur.execute(sql)
        # db.commit()
        cursor = self.db.cursor()
        cursor.execute(sql)
        results = cursor.fetchone()
        return results

    def truncate(self, table):
        sql = 'TRUNCATE TABLE %s' % table
        self.query(sql)

        return

    def find_last(self, table, conditions, order_column, quantity, fields="*"):

        sql = 'select %s from %s where  ' % (fields, table)
        for unit in conditions:
            value = unit[2]
            if type("") == type(value):
                value = "'%s'" % value

            sql = sql + "%s %s %s " % (unit[0], unit[1], value) + "  and "

        if 0 < len(conditions):
            sql = sql[0: -4]
        else:
            sql = sql[:-7]

        sql += 'order by %s DESC limit %s' % (order_column, quantity)

        # 
        res = self.query(sql)
        if res is None:
            return None

        if 0 == len(res):
            return None

        if table not in self._tables:
            self.load_an_table(table)

        if '*' == fields:

            fieldList = self._tables[table]
        else:
            fieldList = fields.split(',')

        # else:
        #     fieldList = str.split(fields)

        self.db.commit()
        return dict(zip(fieldList, res[0]))
