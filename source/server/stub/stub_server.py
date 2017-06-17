import sys

sys.path.append('../../')

from ant.controller.server import *
from ant.controller.handler import *
from ant.controller.xchg import *

from ant.template.manager import *

HANDLER_CONFIG_FILE_PATH = './handler.cfg'
TEMPLATE_DIR = '../static/'

if __name__ == '__main__':

    disp = Dispatcher(
            HANDLER_CONFIG_FILE_PATH,
            TemplateManager({'dir': TEMPLATE_DIR,}),
            None
        )

    server = TcpServer({
            'addr': '127.0.0.1',
            'port': 8888,
            'handler': RequestHandler,
            'dispatcher': disp,
        })

    server.serve()
