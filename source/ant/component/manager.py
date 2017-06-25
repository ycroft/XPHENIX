
from ant.common.log import * 

class ServiceManager(object):

    def __init__(self, handle_list = {}):
        self.handle_list = handle_list
    
    def reg_service(self, name, handle):
        if name in self.handler_list:
            return False
        
        self.handle_list[name] = handle

    def handle(self, request):
        
        log_debug('[service]:handle request: {}.'.format(str(request)))

        if not request:
            log_debug('[service]:do not need to get service response.')
            return

        if request.name in self.handle_list:
            response = self.handle_list[request.name](request.var_list)
            request.write_response(response)

            if not response:
                log_error('return response: {}'.format(request.response.__repr__()))

            log_debug('[service]:get response: {}'.format(request.response.__repr__()))
        else:
            log_error('[service]:handle not found({})'.format(request.name))
            request.write_response(None)
