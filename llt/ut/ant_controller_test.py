import unittest

from ant.controller.server import *
from ant.controller.handler import *
from ant.controller.xchg import *
from ant.common.log import *

class TestTcpServer(unittest.TestCase):
    def test_serve(self):
        server = TcpServer({
            'addr': '127.0.0.1',
            'port': 9999,
            'handler': RequestHandler,
            'dispatcher': None,
        })
        self.assertEqual(0, 0)

class TestDispatcher(unittest.TestCase):

    def test_config_init(self):
        disp = Dispatcher('ut/res/test.cfg', None, None)
        disp.dispatch('127.0.0.1:8888/doczone/login')

        log_debug(disp.req_tmpl)
        log_debug(disp.req_cmpt)
