# coding: utf-8

import os

from ant.template.mod import Mod

class Scanner(object):
    '''扫描器

    用于递归扫描目录下的所有文件，收集模板文件

    Attributes:
        mod_dict: 模板名称--对象字典
    '''
    def __init__(self, scan_dir):
        '''初始化时扫描目录
        '''
        self.mod_dict = {}
        self.scan_mods_text(scan_dir)
        self.scan_mods_ref()

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

                if sufix != 'mod' and sufix != 'html':
                    continue

                file_path = os.path.join(dir_name, file_name)
                mod = Mod(file_path)
                if mod.name == '':
                    raise ScannerVoidModNameError()
                self.mod_dict[mod.name] = mod;
        pass

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

class TemplateManager(object):
    def __init__(self, scanner):
        pass

