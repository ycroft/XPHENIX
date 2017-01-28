
'''异常定义
'''

# 控制模块异常
class ControllerError(Exception): pass
# 配置文件解析错误
class ConfigParseError(ControllerError): pass

