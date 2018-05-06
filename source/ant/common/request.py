
from ant.common.error import *

class REQ_TYPE:
    HTTP, \
    TMPL, \
    CMPT = range(3)

class RSP_TYPE:
    NORMAL, \
    REDIRECT = range(2)

class CommonRequest(object):

    def __init__(self, req_type):
        self.req_type = req_type
        self.rsp_type = RSP_TYPE.NORMAL
        self.var_list = {}
        self.response = None
    
    def add_vars(self, var_list):

        for k, v in var_list.items():

            if k in self.var_list:
                raise ConfigParseError()
            
            self.var_list[k] = v

    def __str__(self):
        return '; '.join([
                'name: {}',
                'request type: {}',
                'response type: {}',
                'var_list: {}',
                'response: {}',
            ]).format(
                self.name,
                self.req_type,
                self.rsp_type,
                self.var_list,
                self.response)

class TemplateRequest(CommonRequest):
    def __init__(self, template_name, is_req_for_mod = True):
        CommonRequest.__init__(self, REQ_TYPE.TMPL)
        self.name = template_name
        self.is_req_for_mod = is_req_for_mod

    def write_response(self, text):
        self.response = text

class ComponentRequest(CommonRequest):
    def __init__(self, component_name):
        CommonRequest.__init__(self, REQ_TYPE.CMPT)
        self.name = component_name

    def write_response(self, args):
        self.response = args

    def set_redirection(self, path):
        self.rsp_type = RSP_TYPE.REDIRECT
        self.add_vars({'__REDIRECT__' : path })

    def get_redir_path(self):
        return self.var_list['__REDIRECT__']
