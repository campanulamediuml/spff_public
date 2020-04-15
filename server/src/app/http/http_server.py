from app.http.relay.relay import Relay
from app.http import mods
import tornado
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from common.Scheduler import Scheduler



class HttpServer(object):

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._apps = self.register_handles()
        Relay.server_init(self)

    def register_handles(self):
        route = mods.create_route()
        return route

    def run(self):
        print("start server")
        print(self._host + ":" + str(self._port))
        tornado.options.parse_command_line()
        http_server = tornado.httpserver.HTTPServer(tornado.web.Application(self._apps))
        # http_server.bind(self._port, self._host)
        # http_server.start(config.thread_num)
        http_server.listen(self._port, self._host)
        tornado.ioloop.PeriodicCallback(Scheduler.run, 500).start()
        tornado.ioloop.IOLoop.current().start()

