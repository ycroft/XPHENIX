# coding: utf-8

'''异常定义
'''

# 控制异常
class ControllerError(Exception): pass
# 配置文件解析异常
class ConfigParseError(ControllerError): pass

# 模板异常
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

# 数据库异常
class DataBaseError(Exception): pass
# 数据库未初始化异常
class DataBaseNotInitError(DataBaseError): pass
