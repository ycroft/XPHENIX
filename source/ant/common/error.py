# coding: utf-8

'''异常定义
'''

# 控制模块异常
class ControllerError(Exception): pass
# 配置文件解析异常
class ConfigParseError(ControllerError): pass

# 模板模块异常
class TemplateError(Exception): pass
# 模板名称缺失异常
class TemplateWithoutNameError(TemplateError): pass
# 模板被多重继承异常
class TemplateMultiInheritError(TemplateError): pass
# 扫描模板出现名字异常
class ScannerVoidModNameError(TemplateError): pass
# 扫描模板出现模板关系异常
class ScannerModRelationError(TemplateError): pass
# 模板元素列表不存在异常
class ElementListNotExistError(TemplateError): pass

class DataBaseError(Exception): pass

class DataBaseNotInitError(DataBaseError): pass
