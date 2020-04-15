from config.config import http_config
from app.http.http_server import HttpServer



if __name__ == '__main__':
    host = http_config['host']
    port = http_config['port']
    print(port)
    server = HttpServer(
        host, 
        port,  
        )
    server.run()




