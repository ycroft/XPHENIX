
class REQ_TYPE:
    HTTP_REQ,
    INTERNAL_REQ = range(2)

class CommonRequest(object):
    __init__(self, req_type):
        self.req_type = req_type
    
    def set_var(self, var_list):
        self.var_list = var_list

