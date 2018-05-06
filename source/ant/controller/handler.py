# coding = utf-8

import BaseHTTPServer

from ant.common.log import *
from ant.controller.mime_type import *

from ant.controller.xchg import ACTION

import os
import urlparse

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    
    keep_alive_url = 'feed_dog'

    def __init__(self, request, client_address, server,
            dispatcher):

        self.dispatcher = dispatcher

        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request,
                client_address, server)

    def _debug_print_context(self):
        log_debug('======================Handle Request======================')
        log_debug('client_address={}'.format(self.client_address))
        log_debug('command={}'.format(self.command))
        log_debug('path={}'.format(self.path))
        log_debug('parsed_path={}'.format(urlparse.urlparse(self.path)))
        log_debug('request_version={}'.format(self.request_version))
        log_debug('headers={}'.format(self.headers))
        log_debug('==========================================================')

    def do_GET(self):

        if self.do_default_filter(): return

        self._debug_print_context()

        '''
        try:
            parsed_path = urlparse.urlparse(self.path).path
            self.dispatcher.dispatch(parsed_path)
            resp_text = self.dispatcher.get_response_text()
            self.fill_normal_header(len(resp_text))
            self.write_context(resp_text)
        except Exception as e:
            log_error("handle url error: {}".format(str(e)))
        '''

        parsed_path = urlparse.urlparse(self.path).path
        result = self.dispatcher.dispatch(parsed_path)

        self.response_with_result(result)
    
    def do_POST(self):
        self._debug_print_context()

        post_data = self.rfile.read(int(self.headers['Content-length']))
        parsed_path = urlparse.urlparse(self.path).path
        
        args = {}
        for k_v in [e.split('=') for e in post_data.split('&')]:
            args[k_v[0]] = k_v[1]
        
        result = self.dispatcher.dispatch(parsed_path, args)

        self.response_with_result(result)
    
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

    def response_with_result(self, result):

        cookie = result.fetch_ctx(ACTION.SET_COOKIE)

        ctx = result.fetch_ctx(ACTION.NORMAL)
        if ctx:
            self.fill_normal_header(len(ctx))

            if cookie:
                self.append_cookies(cookie)

            self.end_headers()
            self.write_context(ctx)
            return

        ctx = result.fetch_ctx(ACTION.REDIRECT)
        if ctx:
            self.fill_redir_header(ctx)

            if cookie:
                self.append_cookies(cookie)

            self.end_headers()
            return
        
        log_error('response exception, reuslt error')

    def fill_redir_header(self, redir_path):
        self.send_response(302)
        mime_type = self.get_mime_type()

        self.send_header('Location', redir_path)
        self.send_header('Content-type', mime_type + '; charset=UTF-8')
        self.send_header('Content-length', 0)

    def fill_normal_header(self, obj_length):

        self.send_response(200)
        mime_type = self.get_mime_type()

        self.send_header('Content-type', mime_type + '; charset=UTF-8')
        self.send_header('Content-length', str(obj_length))

        log_debug('response {} with mime type {}.'.format(self.path, mime_type))
    
    def append_cookies(self, cookie):
        self.send_header('Set-Cookie', cookie.output(header=''))

    def write_context(self, response_str):
        self.wfile.write(response_str)

    def get_mime_type(self):

        parsed_path = urlparse.urlparse(self.path).path
        path, ext = os.path.splitext(parsed_path)

        if not ext:
            return MIME_TYPE_DEFAULT
        
        mime_type = MIME_TYPE_DICT.get(ext, '')

        if mime_type:
            return mime_type
        else:
            return MIME_TYPE_DEFAULT
    
    def send_resp(self, mime_type='text/plain', resp = ''):
        self.send_response(200)
        self.send_header('Content-type', mime_type + '; charset=UTF-8')
        self.send_header('Content-length', str(len(resp)))
        self.end_headers()
        self.wfile.write('')

    def do_default_filter(self):

        ommit_urls = ['/favicon.ico', self.keep_alive_url]

        if self.path in ommit_urls:
            self.send_resp()
            return True
        
        return False
