from app.data.base_method.dbserver.cache import cached_base
    
class Cache(object):
    base = cached_base()

    @staticmethod
    def get_tables():
        return Cache.base.get_tables()

    @staticmethod
    def cache_dumps():
        return Cache.base.cache_dumps()

    @staticmethod
    def find(table,conditions):
        return Cache.base.find(table,conditions)

    @staticmethod
    def select(table, conditions):
        return Cache.base.select(table, conditions)

    @staticmethod
    def insert(table, params):
        return Cache.base.insert(table, params)