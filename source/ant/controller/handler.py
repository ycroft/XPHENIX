
import BaseHTTPServer

from ant.common.log import *

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server,
            dispatcher, merger):

        self.dispatcher = dispatcher
        self.merger = merger

        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request,
                client_address, server)
    
    def do_GET(self):
        log_debug('GET')
        response = 'you are trapped here.'
        self.send_common_headers(len(response))
        self.write_context(response)
    
    def do_POST(self):
        log_debug('POST')
    
    def do_PUT(self):
        log_debug('PUT')

    def do_DELETE(self):
        log_debug('DELETE')
    
    def do_OPTIONS(self):
        log_debug('OPTIONS')
    
    def do_HEAD(self):
        log_debug('HEAD')
    
    def do_TRACE(self):
        log_debug('TRACE')
    
    def do_CONNECT(self):
        log_debug('CONNECT')

    def send_common_headers(self, obj_length):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=UTF-8')
        self.send_header('Content-length', str(obj_length))
        self.end_headers()
    
    def write_context(self, response_str):
        self.wfile.write(response_str)

