# coding: utf-8

'''URL分发
'''
from ant.common.error import *
from ant.common.request import ComponentRequest
from ant.common.request import TemplateRequest
from ant.common.log import *

import ConfigParser
import os
import re

class Dispatcher(object):
    '''URL分发类型

    Attributes:
        config: 配置文件解析器
        req_tmpl: 模板请求缓存
        req_cmpt: 组件
        tmpl: 模板适配对象（用于处理模板请求）
        cmpt: 组件适配对象（用于处理组件请求）
    '''
    def __init__(self, name_cfg, tmpl_adapter, cmpt_adapter):
        '''初始化

        name_cfg: 配置文件路径
        tmpl_adapter: 模板适配对象
        cmpt_adapter: 组件适配对象
        
        '''
        self.config = ConfigParser.ConfigParser()
        if not self.config.read(name_cfg):
            raise ConfigParseError()

        self.req_tmpl = None;       # 目前暂未实现，设为空值
        self.req_cmpt = None;       # 目前暂未实现，设为空值
        self.tmpl = tmpl_adapter
        self.cmpt = cmpt_adapter

    def gen_request_for_html(self, path, post_args):
        '''生成html请求

        解析配置文件，文件规则详见example_handler.cfg

        Args:
            path: 请求路径
            post_args: 传入的额外参数，主要适用于POST请求
        Returns: 无
        Raises:
            ConfigParseError: 解析配置文件错误
        '''
        pageName = ''
        args = {}

        for k, v in self.config.items('page'):
            sres = re.search(v, path)
            if sres:
                pageName = k
                break
        if pageName == '': raise ConfigParseError()     # 遇到未配置的path

        self.req_tmpl = TemplateRequest(self.config.get('template', pageName))
        self.req_cmpt = ComponentRequest(self.config.get('component', pageName))

        if not post_args: return

        var_list = self.config.get('var_list', pageName).split(',')

        if len(var_list) != len(sres.groups()):         # path中的参数个数和配置
            raise ConfigParseError()                    # 中的参数个数不匹配

        for index, var_name in enumerate(var_list):
            var_name = var_name.strip()                 # 处理包含在path中的
            args[var_name] = sres.group(index + 1)      # 传入参数

        for k, v in post_args.items:
            if k in args: raise ConfigParseError()      # POST参数和path参数冲突
            args[k] = v                                 # 用post_args扩展列表

        self.req_tmpl.set_var(args)
        self.req_cmpt.set_var(args)
    
    def gen_request_for_css(self, path):
        '''生成css请求

        单纯导入css的文件名称

        Args:
            path: 请求路径
        Returns: 无
        Raises: 无
        '''
        self.req_tmpl = TemplateRequest('_style_' + path)
        self.req_cmpt = ComponentRequest('')

    def dispatch(self, path, post_args = {}):
        '''分发

        调用模板和组件的处理函数处理打包好的请求

        Args:
            path: 请求路径
            post_args: 传入参数
        Returns: 无
        Raises: 无
        '''
        log_debug('handle path({}) with post({})'.format(path, post_args))

        if path.endswith('css'):
            self.gen_request_for_css(os.path.split(path)[1])
        else:
            self.gen_request_for_html(path, post_args)

        self.tmpl.handle(self.req_tmpl)
        '''
        self.cmpt.handle(self.req_cmpt)

        '''
    
    def conclude_response(self):
        return self.req_tmpl.response

