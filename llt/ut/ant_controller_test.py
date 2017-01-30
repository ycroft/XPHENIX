import unittest

from ant.controller.server import *
from ant.controller.handler import *

class TestTcpServer(unittest.TestCase):
    def test_serve(self):
        server = TcpServer({
            'addr': '127.0.0.1',
            'port': 8888,
            'handler': RequestHandler,
        })
        self.assertEqual(0, 0)

