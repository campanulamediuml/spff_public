import pymysql
from app.data.base_method.Scheduler import IntervalTask
import os

class Base(object):

    def __init__(self, host, user, psw, dbname):
        self._host = host
        self._user = user
        self._psw = psw
        self._dbname = dbname
        self._tables = {}
        self.db = pymysql.connect(host, user, psw, dbname, charset='utf8')

        self._load_tables()

        IntervalTask(300, self.keep_connect)

    def keep_connect(self):
        
        self.query('select 1')

    def connect(self, host, user, psw, dbname):
        self.db = pymysql.connect(self._host, self._user, self._psw, self._dbname, charset='utf8')
        
    # 加载所有数据库表名
    def _load_tables(self):
        sql = 'show tables'
        res = self.query(sql)
        tables = tuple(map(lambda x:x[0], res))
        for table in tables:
            sql = 'show fields from ' + table
            res = self.query(sql)
            self._tables[table] = list(map(lambda x:x[0], res))

    def _load_all_fileds(self):
        pass

    # 查找数据（单条）
    def find(self, table, conditions, fields = '*'):
        sql = 'select %s from %s where ' % (fields, table)
        for unit in conditions:
            value = unit[2]
            if type("") == type(value):
                value = "'%s'" % value

            sql = sql + "%s %s %s " % (unit[0], unit[1], value) + " and "

        if 0 < len(conditions):
            sql = sql[0: -4]

        sql += " limit 1"
        res = self.query(sql)
        if res is None:
            return None

        if 0 == len(res):
            return None

        if '*' == fields:
            fieldList = self._tables[table]
        else:
            fieldList = str.split(fields)

        self.db.commit()
        return dict(zip(fieldList, res[0]))

    # 查找数据
    def select(self, table, conditions, fields='*', order=None):
        sql = 'select %s from %s where  ' % (fields, table)
        for unit in conditions:
            value =  unit[2]
            if type("") == type(value):
                value = "'%s'" % value

            sql = sql + "%s %s %s " % (unit[0], unit[1], value) + " and "

        if 0 < len(conditions):
            sql = sql[0: -4]
        else:
            sql = sql[:-7]

        if order is not None:
            sql += 'order by %s %s ' % (order[0], order[1])

        res = self.query(sql)
        if res is None:
            return None

        if 0 == len(res):
            return None

        if '*' == fields:
            fieldList = self._tables[table]
        else:
            fieldList = str.split(fields)

        result = []
        for data in res:
            data = dict(zip(fieldList, data))
            result.append(data)

        self.db.commit()
        return result

    def insert(self, table, content, isCommit = True):
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
            self.query(sql)
            if True == isCommit:
                self.db.commit()

        return



    def update(self, table, conditions, params, isCommit = True):
        sql = 'update %s set ' % table
        for param, value in params.items():
            if type("") == type(value):
                value = "'%s'" % value
            sql = sql + " %s = %s," % (param, value)

        sql = sql[:-1]
        if len(conditions) > 0:
            sql +=  " where "

        for unit in conditions:
            value = unit[2]
            if type("") == type(value):
                value = "'%s'" % value

            sql = sql + "%s %s %s " % (unit[0], unit[1], value) + " and "

        if 0 < len(conditions):
            sql = sql[0: -4]

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

        self.query(sql)
        if is_commit is True:
            self.db.commit()

        return

    def query(self, sql):
        self.db.ping(reconnect=True)
        # cur.execute(sql)
        # db.commit()
        cursor = self.db.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        return results


    def truncate(self, table):
        sql = 'TRUNCATE TABLE %s'%table
        self.query(sql)

        return
            







