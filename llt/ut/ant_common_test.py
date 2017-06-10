# coding: utf-8

import unittest

import os

from ant.common.dbapi import *
from ant.common.orm import *

class TestDbApi(unittest.TestCase):

    def setUp(self):
        print 'CREATE'
        create_sqlite_engine("test.db")
        with Connection():
            res = db_create_table('user', {
                'name': StringField(len=10, is_pk=True),
                'age': NumberField(),
            })

        self.assertNotEquals(res, None)

    def tearDown(self):
        print 'DESTROY'
        os.system('rm test.db')
        
    def test_db_create_tbl(self):
        with Connection():
            res = db_create_table('user', {
                'name': StringField(len=10, is_pk=True),
                'age': NumberField(),
            })

        # 表已经存在
        self.assertEquals(res, None)
    
    def test_db_insert(self):
        with Connection():
            res = db_insert("user", {'name' : 'john', 'age': 18,})
            self.assertNotEquals(res, None)

            res = db_insert("user", {'name' : 'Venoth', 'age': 19,})
            self.assertNotEquals(res, None)

            res = db_insert("user", {'name' : 'Brown', 'age': 20,})
            self.assertNotEquals(res, None)

            res = db_insert("user", {'name' : 'Kingdren', 'age': 21,})
            self.assertNotEquals(res, None)

            db_delete("user")

    def test_db_query(self):
        with Connection():
            res = db_insert("user", {'name' : 'john', 'age': 18,})
            self.assertNotEquals(res, None)

            res = db_insert("user", {'name' : 'Venoth', 'age': 19,})
            self.assertNotEquals(res, None)

            res = db_insert("user", {'name' : 'Brown', 'age': 20,})
            self.assertNotEquals(res, None)

            res = db_insert("user", {'name' : 'Kingdren', 'age': 21,})
            self.assertNotEquals(res, None)

            res = db_select("user")
            self.assertEquals(len(res), 4)

            res = db_select("user", 'age', "name='john'")
            self.assertEquals(len(res), 1)
            self.assertEquals(res[0][0], 18)

            res = db_select("user", 'age', "name='Venoth'")
            self.assertEquals(len(res), 1)
            self.assertEquals(res[0][0], 19)

            res = db_select("user", 'age', "name='Brown'")
            self.assertEquals(len(res), 1)
            self.assertEquals(res[0][0], 20)

            res = db_select("user", 'age', "name='Kingdren'")
            self.assertEquals(len(res), 1)
            self.assertEquals(res[0][0], 21)

            db_delete("user")
    
    def test_db_delete(self):
        with Connection():
            res = db_insert("user", {'name' : 'john', 'age': 18,})
            self.assertNotEquals(res, None)

            res = db_insert("user", {'name' : 'Venoth', 'age': 19,})
            self.assertNotEquals(res, None)

            res = db_insert("user", {'name' : 'Brown', 'age': 20,})
            self.assertNotEquals(res, None)

            res = db_insert("user", {'name' : 'Kingdren', 'age': 21,})
            self.assertNotEquals(res, None)

            res = db_select("user")
            self.assertEquals(len(res), 4)

            db_delete("user", "name='john'")

            res = db_select("user", 'age', "name='john'")
            self.assertEquals(len(res), 0)

            db_delete("user")

            res = db_select("user")
            self.assertEquals(len(res), 0)

class TestOrm(unittest.TestCase):

    def setUp(self):
        create_sqlite_engine("test.db")
        with Connection():
            res = db_create_table('user', {
                'name': StringField(len=10, is_pk=True),
                'age': NumberField(),
            })

        self.assertNotEquals(res, None)

    def tearDown(self):
        os.system('rm test.db')

    def test_orm_construct(self):
        class User(Model):
            name = StringField(is_pk=True)
            age = NumberField(size=100)

        user_1 = User(name='john', age=18)
        self.assertEquals(user_1['name'], 'john')
        self.assertEquals(user_1['age'], 18)

    def test_orm_insert_and_get(self):
        class User(Model):
            name = StringField(is_pk=True)
            age = NumberField(size=100)

        user_1 = User(name='john', age=18)
        user_1.insert()
        user_res = User.get(name='john')
    