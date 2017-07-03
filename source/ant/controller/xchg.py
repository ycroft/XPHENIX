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
        '''处理html中嵌入的变量

        变量嵌入标签： {{var name}}

        Args:
            html: HTML文本
            args: 包含变量内容的参数，结构：
                'var_name': value,

        Returns:
            str: 返回处理后的HTML

        Raises:
            MergeResponseError: 模板处理错误

        '''
        search_res = PATTERN.r_VAR.findall(html)

        # 如果没有变量标签，原样返回
        if not search_res:
            return html

        var_list = [e for e in search_res]

        args_need = {}
        for var_name in var_list:

            # 变量内容在参数列表里找不到
            if not var_name in args:
                log_error('var({}) not found in service response.'.format(var_name))
                raise MergeResponseError()

            log_debug('{} will be replaced by {}'.format(var_name, args[var_name]))
            args_need['_var_' + var_name] = args[var_name]

        # 替换变量内容
        return PATTERN.r_VAR.sub(r'{_var_\1}', html).format(**args_need)

    def _preproc_lists(self, html, args):
        '''预处理html中的列表

        Args:
            html: HTML文本
            args: 包含列表内容的参数

        Returns:
            None: 不存在列表元素
            dict: 预处理好的列表内容字典，结构：
                'list_name': 内容
        Raises:
            MergeResponseError: 解析错误

        '''
        cursor = 0
        '''列表信息结构:
            'name': [
                    (起始位置, 结束位置),
                    元素列表[...],
                ]
        '''
        list_info = {}
        # 搜索第一个{{sl ...}}
        search_res = PATTERN.r_LIST_START.search(html, cursor)

        if not search_res:
            return None

        while search_res:
            list_name = search_res.group(1)
            cursor = search_res.end()
            list_start = cursor

            log_debug('find list: {}'.format(list_name))

            # 搜索近邻的{{el}} ——结束标签
            search_res = PATTERN.r_LIST_END.search(html, cursor)

            # 找不到结束，起始结束标签不匹配
            if not search_res:
                log_error('list({}) structure is broken.'.format(list_name))
                raise MergeResponseError()
            # 重复的列表名称
            if list_name in list_info:
                log_error('list({}) is repeated.'.format(list_name))
                raise MergeResponseError()
            # 参数列表中没有给出对应的列表信息
            if not list_name in args:
                log_error('list({}) info is not in given args{}.'.format(list_name, args))
                raise MergeResponseError()

            cursor = search_res.start()
            list_end = cursor

            # 搜索列表中的所有元素
            elements = PATTERN.r_LIST_ELE.findall(html, list_start, list_end)
            list_info[list_name] = [(list_start, list_end), elements]

            search_res = PATTERN.r_LIST_START.search(html, cursor)

        log_debug('get list info: {}'.format(list_info))

        if len(args[list_name]) == 0:
            return ''

        # 准备展开列表内容
        prepare_for_replace = {}
        for list_name, list_struct in list_info.items():

            # 取出列表中的所有文本
            content = PATTERN.r_LIST_ELE.sub(r'{}', html[list_struct[0][0] : list_struct[0][1]])

            # 元素个数和参数信息中包含的对应列表中元素个数不一致
            # 元素名称不对应，个数对应即可，元素名称只是在模板中起提示作用
            if len(list_struct[1]) != len(args[list_name][0]):
                log_error('list({}) can not be found in args{}.'.format(list_name, args))
                raise MergeResponseError()

            # 嵌入变量
            repeated_content = "\n".join([content.format(*tl) for tl in args[list_name]])
            prepare_for_replace[list_name] = repeated_content

        return prepare_for_replace

    def _proc_lists(self, html, args):
        '''处理html中嵌入的列表

        列表嵌入标签:
            {{sl}}
                {{ele A}} ... {{ele B}} ... {{ele C}} ... 
            {{el}}

        Args:
            html: HTML文本
            args:
                包含列表内容的参数，结构：
                'list_x': [
                        [A1, B1, C1],
                        [A2, B2, C2],
                        [A3, B3, C3],
                    ],

        Returns:
            str: 返回处理后的HTML

        Raises:
            MergeResponseError: 模板处理错误

        '''

        # 预处理模板，得到列表信息
        # 由于已经预处理过，下文处理不需要考虑解析异常
        list_content = self._preproc_lists(html, args)

        # 不存在需要处理的列表，原样返回
        if not list_content:
            return html

        cursor = 0
        # 找到第一个列表开始位置
        search_res = PATTERN.r_LIST_START.search(html, cursor)
        result = ''
        list_start = list_end = 0
        while search_res:
            list_name = search_res.group(1)
            cursor = search_res.start()
            list_start = cursor
            
            # 将列表中的内容用预处理好的内容拼接上
            result = result + html[list_end : list_start] + list_content[list_name]

            # 找到结束位置
            search_res = PATTERN.r_LIST_END.search(html, cursor)
            cursor = search_res.end()
            list_end = cursor
            elements = PATTERN.r_LIST_ELE.findall(html, list_start, list_end)

            # 尝试下一个起始位置
            search_res = PATTERN.r_LIST_START.search(html, cursor)

        # 尾部拼接
        result = result + html[list_end :]

        return result

    def _preproc_switches(self, html, args):
        '''预处理html中的分支语法

        Args:
            html: HTML文本
            args: 包含列表内容的参数

        Returns:
            None: 不存在分支语句
            list: 预处理好的分支语句信息，结构：
                [
                    'name',
                    (start_pos, end_pos),
                    {
                        'case_name A': (start_pos, end_pos),
                        'case_name B': (start_pos, end_pos),
                        'case_name C': (start_pos, end_pos),
                    }
                ]
            
        Raises:
            MergeResponseError: 解析错误

        '''

        cursor = 0
        switch_tags = PATTERN.r_SWITCH.search(html, cursor)
        switch_info = []

        # 找不到分支语句
        if not switch_tags:
            return None

        # 从第一个分支标签{{sw ...}}开始
        while switch_tags:

            switch_name = switch_tags.group(1)
            cursor = switch_tags.end()
            switch_start = cursor

            # 搜索分支结合标签{{es}}
            switch_tags = PATTERN.r_SWITCH_END.search(html, cursor)

            # 有开始标签没有结束标签
            if not switch_tags:
                log_error('switch({}) structure is broken.'.format(switch_name))
                raise MergeResponseError()
            # 分支信息没有在参数列表中
            if not switch_name in args:
                log_error('switch({}) info is not in given args{}.'.format(switch_name, args))
                raise MergeResponseError()

            cursor = switch_tags.start()
            switch_end = cursor
            switch_info.append([switch_name, (switch_start, switch_end),])

            # 查找下一个起始标签
            switch_tags = PATTERN.r_SWITCH.search(html, cursor)

        # 处理中间的case标签
        for item in switch_info:
            name = item[0]

            cursor = start = item[1][0]
            stop = item[1][1]

            case_tags = PATTERN.r_CASE.search(html, cursor, stop)

            # switch语句中找不到case
            if not case_tags:
                log_error(''.join(['switch({}) structure must have one case at least.',
                        'switch structure starts from {} and ends at {}.',]).format(
                                switch_name, start, stop))
                raise MergeResponseError()

            case_info = {}
            case_start = case_end = 0

            while case_tags:
                cursor = case_tags.end()
                # 第一个case:
                if case_start == 0:
                    case_start = case_end = cursor
                    case_name = case_tags.group(1)
                # 其他case标签:
                else:
                    case_end = case_tags.start()
                    case_info[case_name] = (case_start, case_end)
                    case_start = cursor
                    case_name = case_tags.group(1)

                case_tags = PATTERN.r_CASE.search(html, cursor, stop)

            case_end = stop
            case_info[case_name] = (case_start, case_end)

            # 记录分支信息
            item.append(case_info)

        log_debug('finish collecting switch_info: {}'.format(switch_info))
        return switch_info

    def _proc_switches(self, html, args):
        '''处理html中嵌入的分支标签

        分支语句标签:
            {{sw class}}
                {{case A}}
                    ...
                {{case B}}
                    ...
                {{case C}}
                    ...
            {{es}}

        Args:
            html: HTML文本
            args:
                包含分支信息，结构：
                'class': 'B',

        Returns:
            str: 返回处理后的HTML

        Raises:
            MergeResponseError: 模板处理错误

        '''
        switch_info = self._preproc_switches(html, args)

        # 找不到分支语句，原样返回
        if not switch_info:
            return html

        cursor = 0
        result = ''
        search_res = PATTERN.r_SWITCH.search(html, cursor)
        start = end = cursor

        info_idx = 0

        while search_res:
            name = search_res.group(1)
            cursor = search_res.start()
            start = cursor
            info = switch_info[info_idx]

            # 预处理的名称和后一次遍历的名称不一致（断言）
            if name != info[0]:
                raise MergeResponseError()
            # 参数列表中没有给出对应的分支信息
            if not args[name] in info[2]:
                log_error('args({}) not in the switch({}) with cases({})'.format(args[name], name, info))
                raise MergeResponseError()

            # 取对应分支的内容
            content_info = info[2][args[name]]
            switch_content = html[content_info[0] : content_info[1]]

            # 拼接结果内容
            result = result + html[end : start] + switch_content

            search_res = PATTERN.r_SWITCH_END.search(html, cursor)
            cursor = search_res.end()
            end = cursor

            search_res = PATTERN.r_SWITCH.search(html, cursor)

        # 拼接尾部
        result = result + html[end:]

        return result
    
    def _merge_request(self):

        static_context = self.req_tmpl.response
        active_context = self.req_cmpt.response

        static_context = self._proc_vars(static_context, active_context)
        static_context = self._proc_lists(static_context, active_context)
        static_context = self._proc_switches(static_context, active_context)

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

