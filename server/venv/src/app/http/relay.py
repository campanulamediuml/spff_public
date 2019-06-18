import jieba
class Relay(object):
    server = None

    @staticmethod
    def init(server):
        Relay.server = server
# 服务器核心操作放在这里