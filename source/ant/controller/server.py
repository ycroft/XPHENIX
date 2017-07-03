# coding: utf-8

'''服务器

'''
import SocketServer
import BaseHTTPServer
import httplib

from ant.common.task import Task
from ant.common.log import *

class TcpServer(SocketServer.TCPServer, Task):
    '''Tcp服务器

    一个多线程TCP服务器，重载相关函数和实现方法详见Socketerver.py

    Attributes:
        address: 服务器地址
        port: 服务器服务端口
        handler: 用于处理请求的handler对象
        dispatcher: 用于将请求定位的对象
        merger: 用于处理组件返回值并生成返回报文的对象
    '''

    def __init__(self, server_config):
        self.address = server_config.get('addr', 'localhost')
        self.port = server_config.get('port', 8888)
        self.handler = server_config['handler']         # raise exception
        self.dispatcher = server_config['dispatcher']   # raise exception
        self.model_init(server_config['models'])

        Task.__init__(self)

    def task_start(self, *args, **kwargs):
        SocketServer.TCPServer.__init__(self, (self.address, self.port),
                self.handler)
        self.serve()
    
    def ask_self(self):
        try:
            conn = httplib.HTTPConnection(self.address, self.port)
            conn.request('GET', self.handler.keep_alive_url)
            resp = conn.getresponse()
            if resp.status == 200:
                return True
            else:
                log_warning('ask self fail: response error({})'.format(resp.status))
                return False
            conn.close()
        except Exception as e:
            log_warning('ask self fail: {}'.format(str(e)))
            return False

    def model_init(self, models):
        for mod in models:
            if not mod.create():
                log_emergency('create db error when create table({})'.format(
                        mod.to_str(),
                    ))
            
            log_debug('mod({}) was loaded.'.format(mod.to_str()))

    def serve(self):
        '''启动函数

        进入Server类型的主循环，直接使用TCPServer类型的serve_forever函数

        Args:       无
        Returns:    无
        Raises:     无
        '''
        try:
            self.serve_forever()
        except Exception as e:
            log_error('server start fail.')

    def finish_request(self, request, client_address):
        '''处理一次请求

        通过实例化Handler类型处理请求，BaseHttpRequestHandler类型会在实例化完成
        后自动调用handle()函数处理一次请求。该函数在被process_request函数调用，
        该函数被ThreadingMixIn类型以多线程方式重新实现

        Args:
            request: http请求
            client_address: 客户端地址

        Returns:    无
        Raises:     无
        '''
        self.RequestHandlerClass(
            request,
            client_address,
            self,
            self.dispatcher,
        )
