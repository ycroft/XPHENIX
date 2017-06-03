import sys
sys.path.append('../../../source/')

import sqlite3
from ant.common.error import *
from ant.common.log import *
import threading

class DataBaseField(object):
    def __init__(self, is_pk):
        self.is_pk = False
        pass

class StringField(DataBaseField):
    def __init__(self, len = 255, is_pk = False):
        DataBaseField.__init__(self, is_pk)
        self.str_len = len

class TextField(DataBaseField):
    def __init__(self, is_pk = False):
        DataBaseField.__init__(self, is_pk)
        pass

class NumberField(DataBaseField):
    def __init__(self, size = 9, is_pk = False):
        DataBaseField.__init__(self, is_pk)
        self.size = size

class BoolField(DataBaseField):
    def __init__(self, is_pk = False):
        DataBaseField.__init__(self, is_pk)
        pass

class DateField(DataBaseField):
    def __init__(self, date_type = 'DATE', is_pk = False):
        DataBaseField.__init__(self)
        self.date_type = date_type

class StubConnection(object):
    def connect(self):
        log_debug("connection established.")
        return self

    def cleanup(self):
        log_debug("connection clean up.")

    def get_cursor(self):
        log_debug("return cursor.")

    def execute(self, statement):
        log_debug("excute a sql: {}".format(statement))

class SqliteConnection(object):
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.type_map = {
            StringField : 'TEXT',
            TextField: 'TEXT',
            NumberField: 'REAL',
            BoolField: 'INTEGER',
        }

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self
    
    def cleanup(self):
        self.conn.close()
        self.conn = None
        self.cursor = None

    def get_cursor(self):
        return self.cursor
    
    def execute(self, statement):
        return self.cursor.execute(statement)
    
    def get_type_name(self, field):
        if not type(field) in self.type_map:
            log_error("unkown field type({}).".format(type(field)))
            return ''
        return self.type_map[type(field)]

class DataBaseContext(object):
    def __init__(self, connection):
        self.conn = connection
    
    def connect(self):
        return self.conn.connect()

database_context = None

class ConnectionContext(threading.local):
    def __init__(self):
        self.connHandle = None
        self.sessionIndex = 0
    
    def isInit(self):
        return not self.connHandle is None
    
    def init(self):
        if not database_context:
            raise DataBaseNotInitError()
        self.connHandle = database_context.connect()
        self.sessionIndex = 0
    
    def destroy(self):
        self.connHandle.cleanup()
        self.connHandle = None

    def get_cursor(self):
        return self.connHandle.get_cursor()
    
    def execute(self, sql):
        return self.connHandle.execute(sql)

    def get_type_name(self, field):
        return self.connHandle.get_type_name(field)

connection_context = ConnectionContext()

class Connection(object):
    def __enter__(self):
        global connection_context
        self.lock = True
        if not connection_context.isInit():
            connection_context.init()
            self.lock = False
    
    def __exit__(self, exctype, excvalue, traceback):
        global connection_context   
        if not self.lock:
            connection_context.destroy()

def with_connection(execute_func):
    def _func(*args, **kwargs):
        with Connection():
            return execute_func(*args, **kwargs)
    return _func


def create_stub_engine():
    global database_context
    database_context = DataBaseContext(StubConnection())

def create_sqlite_engine(db_name):
    global database_context
    database_context = DataBaseContext(SqliteConnection(db_name))

def destroy_engine():
    del database_context
    database_context = None

@with_connection
def create_table(table_name, field_dict):
    global connection_context
    name_pair = [(name, connection_context.get_type_name(field)) for name, field in field_dict.items()]
    for e in name_pair:
        if e[1] == '':
            log_error('get db type name error.')
            return
    str_fields = ', '.join([e[0] + ' ' +  e[1] for e in name_pair])
    sql = "CREATE TABLE {} ({})".format(table_name, str_fields)
    log_debug("execute sql(\"{}\")".format(sql))
    try:
        connection_context.execute(sql)
    except Exception as e:
        log_notice("create table failed: " + str(e))

@with_connection
def select(table_name_list, condition = '', columns = '*'):
    global connection_context
    if list == type(table_name_list):
        str_tables = ', '.join(table_name_list)
    else:
        str_tables = table_name_list
    if condition:
        sql = "SELECT {} FROM {} WHERE {}".format(columns, str_tables, condition)
    else:
        sql = "SELECT {} FROM {}".format(columns, str_tables)
    log_debug("execute sql(\"{}\")".format(sql))
    try:
        connection_context.execute(sql)
        return connection_context.get_cursor().fetchall()
    except Exception as e:
        log_notice("select records failed: " + str(e))

@with_connection
def insert(table_name, value_list):
    str_values = ', '.join([e.__repr__() for e in value_list])
    sql = "INSERT INTO {} VALUES({})".format(table_name, str_values)
    log_debug("execute sql(\"{}\")".format(sql))
    try:
        return connection_context.execute(sql)
    except Exception as e:
        log_notice("insert record failed: " + str(e))

if __name__ == '__main__':
    create_stub_engine()
    with Connection():
        select("user")
    create_sqlite_engine("test.db")
    with Connection():
        create_table('user', {
            'name': StringField(10),
            'age': NumberField(),
        })
        insert("user", ['John', 18])
        insert("user", ['Venoth', 27])
        insert("user", ['Brown', 23])
        insert("user", ['Kingdren', 25])
        res = select("user")
        log_notice("query result: " + str(res))
