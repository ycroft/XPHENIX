import unittest

from ant.template.mod import *

class TestMod(unittest.TestCase):
    def test_mod_parser(self):
        m1 = Mod('ut/test_main.html')
        m2 = Mod('ut/test_child.html')
        
        self.assertEqual('main_page_mod', m1.name)
        self.assertEqual('main', m2.name)
        
