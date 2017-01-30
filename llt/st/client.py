
from httplib import HTTPConnection
import urllib

class TestClient(object):

    def __init__(self, addr, port, logFunc):
        self.conn = HTTPConnection(addr, port, timeout = 10)
        self.respCache = None
        self.log = logFunc

    def logResponse(self):
        self.log('[TestClient]Get response.\n'
                'status: {}\n'
                'reason: {}\n'
                '  data: {}\n'.format(
                self.respCache.status,
                self.respCache.reason,
                self.respCache.read()))

    def do_GET(self, request):
        self.conn.request('GET', request)
        self.respCache = self.conn.getresponse()
        self.logResponse()

    def do_POST(self, args, headers):
        params = urllib.urlencode(args)
        self.conn.request('POST', params, headers)
        self.respCache = self.conn.getresponse()
        self.logResponse()

if __name__ == '__main__':
    def common_log(text):
        print text
    client = TestClient('www.baidu.com', 80, common_log)

    client.do_GET('/')

