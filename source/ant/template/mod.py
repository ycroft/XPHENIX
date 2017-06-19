# coding: utf-8

from ant.common.error import *
from ant.common.log import *

import os
import re

class PATTERN:
    '''正则表达式
    '''
    TAG = r'{{{{{tag} ([a-zA-Z_][a-zA-Z0-9_]*)}}}}\n'   # 匹配标签
    
    r_CHILD = re.compile(r'{{ac}}')                     # 子模板嵌入标签
    r_NAME = re.compile(TAG.format(tag='name'))         # 模板名称标签
    r_FROM = re.compile(TAG.format(tag='from'))         # 模板继承标签
    r_INSERT = re.compile(TAG.format(tag='insert'))     # 模板嵌入标签
    r_VAR = re.compile(TAG.format(tag='var'))           # 变量嵌入标签

'''

# 列表变量的推导可以推迟到页面生成时执行

class ElementList(object):
    def __init__(self):
        self.name = ''
        self.ele_list = {}

    def create_element(self, var_name):
        self.ele_list[var_name] = None

    def set_element(self, var_name, value):
        if not var_name in self.ele_list:
            raise ElementListNotExistError()
        self.ele_list[var_name] = value
''' 

class Mod(object):
    '''模板类

    Attributes:
        file_path: 文件名
        parent: 父模板，初始用字符串记，更新引用关系后改为对象引用，以下同
        child_list: 子模板列表
        refered_by: 引用该模板的模板
        ref_list: 引用模板列表
        ele_list: “列表变量”列表
    '''
    def __init__(self, file_path, context=None):
        '''使用文件初始化
        '''
        self.name = ''

        self.parent = None
        self.child_list = []
        self.refered_by = None
        self.ref_list = []
        
        self.ele_list = None

        if None == context:
            self.file_path = file_path
            self.parse_file(file_path)
        else:
            self.context = context

    def _search_tag_name(self):
        '''搜索名字标签

        名字标签为{name ***}，整个模板文件中必须且只能出现一次

        Args:       无
        Returns:    无
        Errors:     无
        '''
        match_res = PATTERN.r_NAME.findall(self.context)

        if 1 != len(match_res):                     # 找不到名字定义
            raise TemplateWithoutNameError()

        self.name = match_res[0]                    # 名字解析后去掉标签
        self.context = PATTERN.r_NAME.sub('', self.context)

    def _search_tag_from(self):
        '''搜索继承标签

        继承标签为{from ***}，整个文件中最多出现一次

        Args:       无
        Returns:    无
        Errors:
            TemplateMultiInheritError: 模板多重继承异常
        '''
        match_res = PATTERN.r_FROM.findall(self.context)
        if 1 < len(match_res):
            raise TemplateMultiInheritError()

        if 0 == len(match_res):
            return

        self.parent = match_res[0]
        self.context = PATTERN.r_FROM.sub('', self.context)

    def _search_tag_child(self):
        '''搜索嵌入标签

        嵌入标签为{ac}，且不用出现子模板名称，这意味着可以有许多模板套用当前
        模板

        Args:       无
        Returns:    无
        Errors:     无
        '''
        match_res = PATTERN.r_CHILD.findall(self.context)
        if 0 == len(match_res):
            self.child_list = None
        else:
            self.child_list = []

    def _search_tag_insert(self):
        '''搜索插入标签

        插入标签为{insert ***}，该标签必须指定模板名字，插入与模板嵌入的区别
        在于一个是主动，一个是被动

        Args:       无
        Returns:    无
        Errors:     无
        '''
        match_res = PATTERN.r_INSERT.findall(self.context)

        if 0 == len(match_res): return              # 没有插入标签

        for ref_name in match_res:
            self.ref_list.append(ref_name)

        ''' prepare to be formatted
        self.context = PATTERN.r_INSERT.sub(r'{_insert_\1}', self.context)
        '''

    def _search_tag_var(self):
        '''搜索单变量标签

        单变量标签为{var ***}，正则表达式搜索并文本替换成{var_***}

        Args:       无
        Returns:    无
        Errors:     无
        '''

        ''' prepare to be formatted
        self.context = PATTERN.r_VAR.sub(r'{_var_\1}', self.context)
        '''
        pass

    def parse_file(self, file_path):
        '''解析文件

        Args:
            file_path: 文件路径
        Returns:    无
        Errors:     无
        '''
        self.mod_file = open(file_path, 'r')
        self.context = self.mod_file.read()

        self._search_tag_name()
        self._search_tag_from()
        self._search_tag_child()
        self._search_tag_insert()
        self._search_tag_var()

    def open_tag_ac(self, cxt):
        '''展开继承标签

        Args:
            cxt: 用于展开的文本 
        Returns:    无
        Errors:     无
        '''
        if self.child_list:
            return PATTERN.r_CHILD.sub(r'{ac}', self.context).format(
                ac=cxt)
        else:
            return cxt

    def open_tag_ref(self):
        '''展开引用标签

        递归打开模板中的引用标签，将引用的文本复制过来，这里没有预防循环引用的
        能力，可能会导致无穷递归，是否有循环依赖应该在扫描模板的时候进行检查

        Args:       无
        Returns:    无
        Errors:     无
        '''
        if len(self.ref_list):
            fmt_dict = {}
            for ref_mod in self.ref_list:
                fmt_dict[ref_mod.name] = ref_mod.open_tag_ref()
            self.context = PATTERN.r_INSERT.sub(r'%(\1)s', self.context)%(fmt_dict)

        return self.context

    def can_be_entry(self):
        '''判断该模板是否可以作为入口
        '''
        if None != self.child_list:
            return False

        if None != self.refered_by:
            return False

        return True

    def __str__(self):
        '''格式化字符串表示以方便日志打印
        '''
        return '\n'.join([
                'mod info:',
                'name: {}',
                'file name: {}',
                'parent: {}',
                'child list: {}',
                'refered by: {}',
                'reference list: {}',
            ]).format(
                self.name,
                self.file_path,
                self.parent.__repr__(),
                self.child_list,
                self.refered_by.__repr__(),
                self.ref_list,
            )

class Scanner(object):
    '''扫描器

    用于递归扫描目录下的所有文件，收集模板文件

    Attributes:
        mod_dict: 模板名称--对象字典
        rsc_dict: 资源名称--资源文件路径
    '''
    def __init__(self, scan_dir, mod_dict = {}, rsc_dict = {}):
        '''初始化时扫描目录
        '''
        self.mod_dict = mod_dict
        self.rsc_dict = rsc_dict
        self.scan_mods_text(scan_dir)
        self.scan_mods_ref()
        self.check_mods_ref()
        self.open_mods_ref()
        self.scan_rsc(scan_dir)

        log_debug(('[template] manager initialized.' +
            'dir({}), mod dict({}), css dict({}).').format(
                scan_dir,
                str(self.mod_dict),
                str(self.rsc_dict),
            ))

    def scan_mods_text(self, scan_dir):
        '''扫描文本

        扫描后缀名为mod或html的文件文本作为模板对象，并通过模板名称建立引用字典

        Args:
            scan_dir: 扫描目录路径名称
        Returns: 无
        Errors:
            ScannerVoidModNameError: 扫描模板名称异常
        '''
        for dir_name, sub_dir_list, file_list in os.walk(scan_dir):
            for file_name in file_list:
                sufix = os.path.splitext(file_name)[1][1:]

                if not self.is_mods(sufix):
                    continue

                file_path = os.path.join(dir_name, file_name)

                log_debug('[template]: scan a mod file({}).'.format(file_path))
                mod = Mod(file_path)
                if mod.name == '':
                    raise ScannerVoidModNameError()
                self.mod_dict[mod.name] = mod
        pass
    
    def scan_rsc(self, scan_dir):
        '''扫描资源文件

        模板以外的资源的文件，仅获取路径

        Args:
            scan_dir: 扫描目录路径名称
        Returns: 无
        Errors: 无
        '''

        for dir_name, sub_dir_list, file_list in os.walk(scan_dir):
            for file_name in file_list:
                sufix = os.path.splitext(file_name)[1][1:]

                if self.is_mods(sufix):
                    continue

                file_path = os.path.join(dir_name, file_name)

                self.rsc_dict[file_name] = file_path

    def scan_mods_ref(self):
        '''建立模板引用

        扫描模板对象引用字典，建立引用关系，即用对象引用替代原来对象中的字符串
        记录。

        Args: 无
        Returns: 无
        Errors:
            ScannerModRelationError: 模板引用关系异常
        '''
        try:
            for mod_name, mod in self.mod_dict.items():
                if mod.parent != None:
                    mod.parent = self.mod_dict[mod.parent]
                    mod.parent.child_list.append(mod)
                if 0 != len(mod.ref_list):
                    for ref_name in mod.ref_list:
                        self.mod_dict[ref_name].refered_by = mod
                    for index, ref_name in enumerate(mod.ref_list):
                        mod.ref_list[index] = self.mod_dict[ref_name]
        except e:
            raise ScannerModRelationError()

    def check_mods_ref(self):
        '''检查模板引用

        被引用的模板中应不存在其他继承关系

        Args:       无
        Returns:    无
        Errors:
            TemplateMultiInheritError: 模板多重继承异常
        '''
        for mod_name, mod in self.mod_dict.items():
            if mod.refered_by and mod.parent:
                raise TemplateMultiInheritError()

    def open_mods_ref(self):
        '''扩展所有模板的引用

        Args:       无
        Returns:    无
        Errors:     无
        '''
        for mod_name, mod in self.mod_dict.items():
            mod.open_tag_ref()

    def generate_html(self, name):
        '''生成HTML

        Args:
            name: 模板名称
        Returns:    无
        Errors:     无
        '''
        if not name in self.mod_dict:
            # debug info
            return ''
        if not self.mod_dict[name].can_be_entry():
            # debug info
            return ''
        
        mod_cursor = self.mod_dict[name]
        current_context = mod_cursor.context
        while mod_cursor:
            current_context = mod_cursor.open_tag_ac(current_context)
            mod_cursor = mod_cursor.parent

        return current_context

    def generate_rsc(self, name):
        '''读取资源文件内容

        Args:
            name: 资源文件名称

        Returns:    无
        Errors:     无
        '''
        file_path = self.rsc_dict[name]          # raise exception

        file_handle = open(file_path, 'r')

        log_debug('resource file open({}) at {}.'.format(file_path, file_handle))

        ctxt = file_handle.read()
        if not ctxt:
            log_error('file({}) with no content.'.format(file_path))
        file_handle.close()

        return ctxt
    
    def is_mods(self, sufix):
        if sufix == 'mod' or sufix == 'html':
            return True

        return False

