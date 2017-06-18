# coding: utf-8

from ant.template.mod import Mod
from ant.template.mod import Scanner

from ant.common.log import *

class TemplateManager(object):
    def __init__(self, tmpl_config):
        self.mod_dict = {}
        self.css_dict = {}
        self.mod_dir = tmpl_config['dir']
        self.scanner = Scanner(self.mod_dir, self.mod_dict, self.css_dict)

    def handle(self, request):
        log_debug('[template]:handle request: {}.'.format(str(request)))

        if request.name.startswith('_style_'):
            css_name = request.name.replace('_style_', '')
            request.write_response(self.scanner.generate_css(css_name))
        else:
            request.write_response(self.scanner.generate_html(request.name))
