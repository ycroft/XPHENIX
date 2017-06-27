import sys

sys.path.append('../../')

from ant.controller.server import *
from ant.controller.handler import *
from ant.controller.xchg import *

from ant.template.manager import *

from ant.component.manager import *

from ant.common.task import Monitor

from backend import *

HANDLER_CONFIG_FILE_PATH = './handler.cfg'
TEMPLATE_DIR = '../../static/'

if __name__ == '__main__':

    disp = Dispatcher(
            HANDLER_CONFIG_FILE_PATH,
            TemplateManager({'dir': TEMPLATE_DIR,}),
            ServiceManager({
                    'backend_login': handle_page_login,
                    'backend_control_panel': handle_page_control_panel,
                    'user_login': handle_action_login,
                })
        )

    server = TcpServer({
            'addr': '127.0.0.1',
            'port': 8888,
            'handler': RequestHandler,
            'dispatcher': disp,
        })

    monitor = Monitor(server)
    monitor.start_and_watch()

