
from ant.common.log import * 

class ServiceManager(object):

    def __init__(self, config):
        self.handler = config['handler']
    
    def reg_service(self, name, handle):
        if name in self.handler_list:
            return False
        
        self.handle_list[name] = handle

    def handle(self, request):
        
        log_debug('[service]:handle request: {}.'.format(str(request)))

        if not request:
            log_debug('[service]:do not need to get service response.')
            return

        if request.name in dir(self.handler):
            response = eval('self.handler.' + request.name + '(request.var_list)')

            if 'TYPE' not in response:
                log_error('response borken {}', response)
                request.write_response(None)
                return

            if response['TYPE'] == 'normal':
                request.write_response(response['VALUES'])
            elif response['TYPE'] == 'redirect' :
                request.set_redirection(response['PATH'])
            else:
                log_error('invalid response {}', response)
            
            if 'COOKIE' in response:
                request.set_cookie(response['COOKIE'])

            if not response:
                log_error('return response: {}'.format(request.response.__repr__()))

            log_debug('[service]:get response: {}'.format(request.response.__repr__()))
        else:
            log_error('[service]:handle not found({})'.format(request.name))
            request.write_response(None)
