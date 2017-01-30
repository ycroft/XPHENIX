# coding: utf-8

from ant.common.error import *
import re

class PATTERN:
    '''正则表达式
    '''
    TAG = r'{{{tag} ([a-zA-Z_][a-zA-Z0-9_]*)}}\n'       # 匹配标签
    
    r_CHILD = re.compile(r'\{ac\}')                     # 子模板嵌入标签
    r_NAME = re.compile(TAG.format(tag='name'))         # 模板名称标签
    r_FROM = re.compile(TAG.format(tag='from'))         # 模板继承标签
    r_INSERT = re.compile(TAG.format(tag='insert'))     # 模板嵌入标签

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
    def __init__(self, file_path):
        '''默认初始化
        '''
        self.file_path = file_path
        self.name = ''

        self.parent = None
        self.child_list = []
        self.refered_by = None
        self.ref_list = []
        
        self.ele_list = None

        self.parse_file(file_path)

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
        Errors:     无
        '''
        match_res = PATTERN.r_FROM.findall(self.context)
        if 1 < len(match_res):
            raise TemplateMultiInheritError()

        if 0 == len(match_res):
            return

        self.parent = match_res[0]

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

    def parse_file(self, file_path):
        '''解析文件
        '''
        self.mod_file = open(file_path, 'r')
        self.context = self.mod_file.read()

        self._search_tag_name()
        self._search_tag_from()
        self._search_tag_child()
        self._search_tag_insert()

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


