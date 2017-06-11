import unittest

from ant.template.mod import *
from ant.template.manager import *
from ant.common.log import *

def _debug_(info):
    print '\n'.join([
            '***** debug *****',
            info.__str__(),
            '****** end ******',
            '',
        ])

class TestMod(unittest.TestCase):
    def test_mod_parser(self):
        m1 = Mod('ut/res/test_main.mod')
        m2 = Mod('ut/res/test_child.mod')
        
        self.assertEqual('main_page_mod', m1.name)
        self.assertEqual('main', m2.name)

    def test_scanner(self):
        s = Scanner('ut/res/')
        self.assertEqual(4, len(s.mod_dict))
        log_debug(s.generate_html('main'))
        '''
        for name, mod in s.mod_dict.items():
            _debug_(mod)
        _debug_(s.mod_dict['main_page_mod'].context)
        '''

    def test_manager(self):
        tm = TemplateManager({
                'dir': 'ut/res/',
            })
        self.assertEqual(4, len(tm.mod_dict))
        '''
        _debug_(tm.mod_dict)
        '''
        
