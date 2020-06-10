from copy import deepcopy


class Cache(object):
    table_index = {}

    @staticmethod
    def update_table(table,data):
        if data == None:
            return
        res = {}
        for line in data:
            if 'id' in line:
                res[line['id']] = line

        Cache.table_index[table] = res
        # print(Cache.table_index)

    @staticmethod
    def get_table(table,safe):
        if table in Cache.table_index:
            data = Cache.table_index[table]
            if safe is True:
                return Cache.copy_data(data)

            return data
        return

    @staticmethod
    def copy_data(data):
        res = {}
        for k, v in data.items():
            tmp = {}
            for k1, v1, in v.items():
                tmp[k1] = v1
            res[k] = tmp

        return res