import jieba
class Relay(object):
    server = None

    def init(server):
        Relay.server = server
        _initial_split_word = list(jieba.cut_for_search('服务器操作'))
# 服务器核心操作放在这里