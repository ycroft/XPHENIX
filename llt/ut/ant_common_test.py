# coding: utf-8

import unittest

import os

from ant.common.dbapi import *
from ant.common.orm import *

class TestDbApi(unittest.TestCase):

    def setUp(self):
        log_debug('testcase setup: create \'test.db\'')
        create_sqlite_engine("test.db")
        with Connection():
            res = db_create_table('user', {
                'name': StringField(len=10, is_pk=True),
                'age': NumberField(),
            })

        self.assertNotEquals(res, None)

    def tearDown(self):
        log_debug('testcase tear down: remove \'test.db\'')
        os.system('rm test.db')
        
    def test_db_create_tbl(self):
        with Connection():
            res = db_create_table('user', {
                'name': StringField(len=10, is_pk=True),
                'age': NumberField(),
            })

        # 表已经存在
        self.assertNotEquals(res, None)
    
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

class User(Model):
    user_id = NumberField(size=100, is_pk=True, auto_inc=True)
    name = StringField()
    # name = StringField(is_pk=True)
    age = NumberField(size=100)

class TestOrm(unittest.TestCase):

    def setUp(self):
        log_debug('testcase setup: create \'test.db\'')
        create_sqlite_engine("test.db")

        User.create()

        """
        with Connection():
            res = db_create_table('user', {
                'name': StringField(len=10, is_pk=True),
                'age': NumberField(),
            })
        
        self.assertNotEquals(res, None)
        """

    def tearDown(self):
        log_debug('testcase tear down: remove \'test.db\'')
        os.system('rm test.db')

    def test_orm_construct(self):
        user_1 = User(name='john', age=18)
        self.assertEquals(user_1['name'], 'john')
        self.assertEquals(user_1['age'], 18)

    def test_orm_insert_and_get(self):

        user = User(name='john', age=18)
        user.insert()
        user = User(name='dwell', age=29)
        user.insert()
        user = User(name='bob', age=23)
        user.insert()

        users = User.find_all(name='john')
        self.assertEquals(len(users), 1)
        self.assertEquals(users[0]['age'], 18)

        users = User.find_all(name='bob')
        self.assertEquals(len(users), 1)
        self.assertEquals(users[0]['age'], 23)

        user = User.find_one(age=19)
        self.assertEquals(user, None)

        user = User.find_one(age=29)
        self.assertEquals(user['name'], 'dwell')
    
