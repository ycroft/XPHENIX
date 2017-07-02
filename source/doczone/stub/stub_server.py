import sys

sys.path.append('../../')

from ant.controller.server import *
from ant.controller.handler import *
from ant.controller.xchg import *

from ant.template.manager import *

from ant.component.manager import *

from ant.common.dbapi import create_sqlite_engine
from ant.common.task import Monitor

import backend
from doczone.mod.models import MODEL_LIST

HANDLER_CONFIG_FILE_PATH = './handler.cfg'
TEMPLATE_DIR = '../../static/'
DATA_BASE_FILE = './stub_db'

if __name__ == '__main__':

    create_sqlite_engine(DATA_BASE_FILE)

    disp = Dispatcher(
            HANDLER_CONFIG_FILE_PATH,
            TemplateManager({'dir': TEMPLATE_DIR,}),
            ServiceManager({'handler': backend,}),
        )

    server = TcpServer({
            'addr': '127.0.0.1',
            'port': 8888,
            'models': MODEL_LIST,
            'handler': RequestHandler,
            'dispatcher': disp,
        })

    monitor = Monitor(server)
    monitor.start_and_watch()

