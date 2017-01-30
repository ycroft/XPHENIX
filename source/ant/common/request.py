
class REQ_TYPE:
    HTTP, \
    TMPL, \
    CMPT = range(3)

class CommonRequest(object):
    def __init__(self, req_type):
        self.req_type = req_type
        self.var_list = {}
        self.response = None
    
    def set_var(self, var_list):
        self.var_list = var_list

    def __str__(self):
        return '\n'.join([
                'name: {}',
                'request type: {}',
                'var_list: {}',
                'response: {}',
            ]).format(
                self.name,
                self.req_type,
                self.var_list,
                self.response)

class TemplateRequest(CommonRequest):
    def __init__(self, template_name):
        CommonRequest.__init__(self, REQ_TYPE.TMPL)
        self.name = template_name

    def write_response(self, text):
        self.response = text

class ComponentRequest(CommonRequest):
    def __init__(self, component_name):
        CommonRequest.__init__(self, REQ_TYPE.CMPT)
        self.name = component_name

    def write_response(self, args):
        self.response = args

