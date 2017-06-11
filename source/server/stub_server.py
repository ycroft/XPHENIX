import sys

sys.path.append('../')

from ant.controller.server import *
from ant.controller.handler import *

if __name__ == '__main__':
    server = TcpServer({
            'addr': '127.0.0.1',
            'port': 8888,
            'handler': RequestHandler,
        })
    server.serve()
