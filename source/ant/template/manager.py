# coding: utf-8

from ant.template.mod import Mod
from ant.template.mod import Scanner

from ant.common.log import *

class TemplateManager(object):
    def __init__(self, tmpl_config):
        self.mod_dict = {}
        self.rsc_dict = {}
        self.mod_dir = tmpl_config['dir']
        self.scanner = Scanner(self.mod_dir, self.mod_dict, self.rsc_dict)

    def handle(self, request):
        log_debug('[template]:handle request: {}.'.format(str(request)))

        if not request:
            log_debug('[template]:do not request for template.')
            return

        if not request.is_req_for_mod:
            request.write_response(self.scanner.generate_rsc(request.name))

            if not request.response:
                log_error('return response: {}'.format(request.response.__repr__()))
        else:
            request.write_response(self.scanner.generate_html(request.name))
            
            if not request.response:
                log_error('return response: {}'.format(request.response.__repr__()))
