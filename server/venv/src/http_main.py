from config import SERVER
from app.http.http_server import HttpServer


if __name__ == '__main__':
    http_data = SERVER['HTTP']
    host = http_data['host']
    port = http_data['port']
    print(port)
    server = HttpServer(
        host, 
        port,  
        )
    server.run()




