
import BaseHTTPServer

def _debug_(str):
    print(str)

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server,
            dispatcher, merger):

        self.dispatcher = dispatcher
        self.merger = merger

        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request,
                client_address, server)
    
    def do_GET(self):
        _debug_('GET')
        response = 'you are trapped here.'
        self.send_common_headers(len(response))
        self.write_context(response)
    
    def do_POST(self):
        _debug_('POST')
    
    def do_PUT(self):
        _debug_('PUT')

    def do_DELETE(self):
        _debug_('DELETE')
    
    def do_OPTIONS(self):
        _debug_('OPTIONS')
    
    def do_HEAD(self):
        _debug_('HEAD')
    
    def do_TRACE(self):
        _debug_('TRACE')
    
    def do_CONNECT(self):
        _debug_('CONNECT')

    def send_common_headers(self, obj_length):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=UTF-8')
        self.send_header('Content-length', str(obj_length))
        self.end_headers()
    
    def write_context(self, response_str):
        self.wfile.write(response_str)

