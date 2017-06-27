# coding: utf-8

'''URL分发
'''
from ant.common.error import *
from ant.common.request import ComponentRequest
from ant.common.request import TemplateRequest
from ant.common.log import *

from ant.template.mod import PATTERN

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

    def gen_request(self, path, post_args):
        '''生成html请求

        解析配置文件，文件规则详见example_handler.cfg

        Args:
            path: 请求路径
            post_args: 传入的额外参数，主要适用于POST请求
        Returns: 无
        Raises:
            ConfigParseError: 解析配置文件错误
        '''
        rsc_name = ''

        for k, v in self.config.items('page'):
            sres = re.search(v, path)
            if not sres:
                continue

            if sres.end() == len(path):                 # 完全匹配，路由模板
                rsc_name = k
                break
            else:                                       # 请求其他资源
                rsc_name = os.path.split(path)[1]
                self.req_tmpl = TemplateRequest(rsc_name, False)
                self.req_cmpt = None
                return

        if rsc_name == '':                              # 请求资源不存在
            raise TemplateWithoutNameError()

        self.req_tmpl = TemplateRequest(self.config.get('template', rsc_name))
        self.req_cmpt = ComponentRequest(self.config.get('component', rsc_name))

        if post_args:
            self.req_tmpl.add_vars(post_args)
            self.req_cmpt.add_vars(post_args)

        if not self.config.has_option('var_list', rsc_name):
            return

        var_list = self.config.get('var_list', rsc_name).split(',')

        if len(var_list) != len(sres.groups()):         # path中的参数个数和配置
            raise ConfigParseError()                    # 中的参数个数不匹配

        args = {}
        for index, var_name in enumerate(var_list):
            var_name = var_name.strip()                 # 处理包含在path中的
            args[var_name] = sres.group(index + 1)      # 传入参数

        self.req_tmpl.add_vars(args)
        self.req_cmpt.add_vars(args)
    
    def _proc_vars(self, html, args):
        search_res = PATTERN.r_VAR.findall(html)

        if not search_res:
            return html

        var_list = [e for e in search_res]

        args_need = {}
        for var_name in var_list:

            if not var_name in args:
                log_error('var({}) not found in service response.'.format(var_name))
                raise MergeResponseError()

            log_debug('{} will be replaced by {}'.format(var_name, args[var_name]))
            args_need['_var_' + var_name] = args[var_name]

        return PATTERN.r_VAR.sub(r'{_var_\1}', html).format(**args_need)

    def _preproc_lists(self, html, args):
        cursor = 0
        list_info = {}
        search_res = PATTERN.r_LIST_START.search(html, cursor)

        if not search_res:
            return None

        while search_res:
            list_name = search_res.group(1)
            cursor = search_res.end()
            list_start = cursor

            log_debug('find list: {}'.format(list_name))

            search_res = PATTERN.r_LIST_END.search(html, cursor)

            if not search_res:
                log_error('list({}) structure is broken.'.format(list_name))
                raise MergeResponseError()
            if list_name in list_info:
                log_error('list({}) is repeated.'.format(list_name))
                raise MergeResponseError()
            if not list_name in args:
                log_error('list({}) info is not in given args{}.'.format(list_name, args))
                raise MergeResponseError()

            cursor = search_res.start()
            list_end = cursor
            elements = PATTERN.r_LIST_ELE.findall(html, list_start, list_end)
            list_info[list_name] = [(list_start, list_end), elements]

            search_res = PATTERN.r_LIST_START.search(html, cursor)

        log_debug('get list info: {}'.format(list_info))
        prepare_for_replace = {}
        for list_struct in list_info.items():

            content = PATTERN.r_LIST_ELE.sub(r'{}', html[list_struct[0][0] : list_struct[0][1]])
            if len(list_struct[1]) != len(args[list_name]):
                log_error('list({}) and args{} does not have the same length.'.format(list_name, args))
                raise MergeResponseError()

            repeated_content = "\n".join([content.format(tl) for tl in args[list_name]])
            prepare_for_replace[list_name] = repeated_content

        return prepare_for_replace

    def _proc_lists(self, html, args):
        
        list_content = self._preproc_lists(html, args)

        if not list_content:
            return html

        cursor = 0
        search_res = PATTERN.r_LIST_START.search(html, cursor)
        result = ''
        list_start = list_end = 0
        while search_res:
            list_name = search_res.group(0)
            cursor = search_res.start()
            list_start = cursor
            
            result += result + html[list_end : list_start] + list_content[list_name]

            search_res = PATTERN.r_LIST_END.search(html, cursor)
            cursor = search_res.end()
            list_end = cursor
            elements = PATTERN.r_LIST_ELE.findall(html, list_start, list_end)
            list_info[list_name] = [(list_start, list_end), elements]
            search_res = PATTERN.r_LIST_START.search(html, cursor)

        return result
    
    def _merge_request(self):

        static_context = self.req_tmpl.response
        active_context = self.req_cmpt.response

        static_context = self._proc_vars(static_context, active_context)
        static_context = self._proc_lists(static_context, active_context)

        return static_context
    
    def conclude_result(self):
        if not self.req_tmpl.response:
            log_error('Dispatcher: try to conclude void response text.')
            return ''
        
        if (not self.req_cmpt) or (not self.req_cmpt.response):
            return self.req_tmpl.response
        
        return self._merge_request()

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

        self.gen_request(path, post_args)

        self.tmpl.handle(self.req_tmpl)
        self.cmpt.handle(self.req_cmpt)

    def get_response_text(self):

        content = self.conclude_result()
        if content:
            return content
        else:
            log_error('try to get void response({})'.format(
                    content
                ))
            return ''

