# coding: utf-8

import unittest

import os

from ant.common.dbapi import *

class TestDbApi(unittest.TestCase):

    def setUp(self):
        create_sqlite_engine("test.db")
        with Connection():
            res = create_table('user', {
                'name': StringField(len=10, is_pk=True),
                'age': NumberField(),
            })

        self.assertNotEquals(res, None)

    def tearDown(self):
        os.system('rm test.db')
        
    def test_db_create_tbl(self):
        with Connection():
            res = create_table('user', {
                'name': StringField(len=10, is_pk=True),
                'age': NumberField(),
            })

        # 表已经存在
        self.assertEquals(res, None)
    
    def test_db_insert(self):
        with Connection():
            res = insert("user", {'name' : 'john', 'age': 18,})
            self.assertNotEquals(res, None)

            res = insert("user", {'name' : 'Venoth', 'age': 19,})
            self.assertNotEquals(res, None)

            res = insert("user", {'name' : 'Brown', 'age': 20,})
            self.assertNotEquals(res, None)

            res = insert("user", {'name' : 'Kingdren', 'age': 21,})
            self.assertNotEquals(res, None)

            delete("user")

    def test_db_query(self):
        with Connection():
            res = insert("user", {'name' : 'john', 'age': 18,})
            self.assertNotEquals(res, None)

            res = insert("user", {'name' : 'Venoth', 'age': 19,})
            self.assertNotEquals(res, None)

            res = insert("user", {'name' : 'Brown', 'age': 20,})
            self.assertNotEquals(res, None)

            res = insert("user", {'name' : 'Kingdren', 'age': 21,})
            self.assertNotEquals(res, None)

            res = select("user")
            self.assertEquals(len(res), 4)

            res = select("user", name='john')
            self.assertEquals(len(res), 1)

            res = select("user", name='Venoth')
            self.assertEquals(len(res), 1)

            res = select("user", name='Brown')
            self.assertEquals(len(res), 1)

            res = select("user", name='Kingdren')
            self.assertEquals(len(res), 1)

            delete("user")
    
    def test_db_delete(self):
        with Connection():
            res = insert("user", {'name' : 'john', 'age': 18,})
            self.assertNotEquals(res, None)

            res = insert("user", {'name' : 'Venoth', 'age': 19,})
            self.assertNotEquals(res, None)

            res = insert("user", {'name' : 'Brown', 'age': 20,})
            self.assertNotEquals(res, None)

            res = insert("user", {'name' : 'Kingdren', 'age': 21,})
            self.assertNotEquals(res, None)

            res = select("user")
            self.assertEquals(len(res), 4)

            delete("user", name='john')

            res = select("user", name='john')
            self.assertEquals(len(res), 0)

            delete("user")

            res = select("user")
            self.assertEquals(len(res), 0)
