# coding = utf-8

import BaseHTTPServer

import urlparse

from ant.common.log import *

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server,
            dispatcher, merger):

        self.dispatcher = dispatcher
        self.merger = merger

        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request,
                client_address, server)
    
    def _debug_print_context(self):
        log_debug('client_address={}'.format(self.client_address))
        log_debug('command={}'.format(self.command))
        log_debug('path={}'.format(self.path))
        log_debug('parsed_path={}'.format(urlparse.urlparse(self.path)))
        log_debug('request_version={}'.format(self.request_version))
        log_debug('headers={}'.format(self.headers))

    def do_GET(self):
        self._debug_print_context()

        try:
            self.dispatcher.dispatch(self.path)
            print self.dispatcher.req_tmpl
            print self.dispatcher.req_cmpt
        except Exception as e:
            log_error("handle url error: {}".format(str(e)))
        
        response = 'you are trapped here.'
        self.send_common_headers(len(response))
        self.write_context(response)
    
    def do_POST(self):
        pass
    
    def do_PUT(self):
        pass

    def do_DELETE(self):
        pass
    
    def do_OPTIONS(self):
        pass
    
    def do_HEAD(self):
        pass
    
    def do_TRACE(self):
        pass
    
    def do_CONNECT(self):
        pass

    def send_common_headers(self, obj_length):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=UTF-8')
        self.send_header('Content-length', str(obj_length))
        self.end_headers()
    
    def write_context(self, response_str):
        self.wfile.write(response_str)

