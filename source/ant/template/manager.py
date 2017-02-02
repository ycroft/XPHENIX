# coding: utf-8

from ant.template.mod import Mod
from ant.template.mod import Scanner

class TemplateManager(object):
    def __init__(self, tmpl_config):
        self.mod_dict = {}
        self.mod_dir = tmpl_config['dir']
        self.scanner = Scanner(self.mod_dir, self.mod_dict)

    def generate_html(self, name):
        return self.scanner.generate_html(name)

