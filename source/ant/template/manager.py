# coding: utf-8

from ant.template.mod import Mod
from ant.template.mod import Scanner
from ant.controller.xchg import RESOURCE_FILE_TAG

from ant.common.log import *

class TemplateManager(object):
    def __init__(self, tmpl_config):
        self.mod_dict = {}
        self.rsc_dict = {}
        self.mod_dir = tmpl_config['dir']
        self.scanner = Scanner(self.mod_dir, self.mod_dict, self.rsc_dict)

    def handle(self, request):
        log_debug('[template]:handle request: {}.'.format(str(request)))

        if request.name.startswith(RESOURCE_FILE_TAG):
            rsc_name = request.name.replace(RESOURCE_FILE_TAG, '')
            print rsc_name
            print self.rsc_dict
            request.write_response(self.scanner.generate_rsc(rsc_name))
        else:
            request.write_response(self.scanner.generate_html(request.name))
