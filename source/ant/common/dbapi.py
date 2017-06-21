# coding: utf-8

'''数据库接口
'''

import sqlite3
import threading

from ant.common.error import *
from ant.common.log import *

class DataBaseField(object):
    def __init__(self, is_pk):
        self.is_pk = False
        pass

class StringField(DataBaseField):
    def __init__(self, **args):
        DataBaseField.__init__(self, args.get('is_pk', False))
        self.str_len = args.get('len', 255)
        self.str_le = len

class TextField(DataBaseField):
    def __init__(self, **args):
        DataBaseField.__init__(self, args.get('is_pk', False))

class NumberField(DataBaseField):
    def __init__(self, **args):
        DataBaseField.__init__(self, args.get('is_pk', False))
        self.size = args.get('size', 255)

class BoolField(DataBaseField):
    def __init__(self, **args):
        DataBaseField.__init__(self, args.get('is_pk', False))

class DateField(DataBaseField):
    def __init__(self, **args):
        DataBaseField.__init__(self, args.get('is_pk', False))
        self.date_type = args.get('data_type', 'DATA')

class StubConnection(object):
    '''桩数据库连接对象

    用于桩测，无功能用途

    Attributes:     无
    '''
    def connect(self):
        '''【桩】建链函数

        Args:       无
        Returns:
            SubConnection: 返回自身引用
        Raises:     无
        '''
        log_debug("connection established.")
        return self

    def cleanup(self):
        '''【桩】清理函数

        Args:       无
        Returns:    无
        Raises:     无
        '''
        log_debug("connection clean up.")

    def get_cursor(self):
        '''【桩】获取句柄函数

        Args:       无
        Returns:    无
        Raises:     无
        '''
        log_debug("return cursor.")
 
    def execute(self, statement):
        '''【桩】执行SQL函数

        Args:
            statement: SQL语句
        Returns:    无
        Raises:     无
        '''
        log_debug("execute a sql: {}".format(statement))

    def commit(self):
        '''【桩】提交函数

        Args:       无
        Returns:    无
        Raises:     无
        '''
        log_debug("actions commited.")
    

class SqliteConnection(object):
    '''Sqlite数据库连接对象

    用于适配Sqlite数据库的python接口

    Attributes:
        db_name: Sqlite数据库名称
        conn: 数据库连接句柄
        cursor: Sqlite数据库游标
        type_map: 类型映射，用于将定义的基本类型映射到对应的Sqlite数据类型的
            字段名称
    '''

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
        '''建链函数

        调用sqlite3的connect接口进行建链

        Args:       无
        Returns:
            SqliteConnection: 返回自身引用

        Raises:
            @exception_from: sqlite3.connect
        '''
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self

    def cleanup(self):
        '''关闭sqlite连接

        Args:       无
        Returns:    无
        Raises:
            @exception_from: <sqlite3.Connection>.close
        '''
        self.conn.close()
        self.conn = None
        self.cursor = None

    def get_cursor(self):
        '''得到sqlite游标

        Args:       无
        Returns:
            sqlite3.Cursor: 游标对象

        Raises: 	无
        '''
        return self.cursor
    
    def execute(self, statement):
        '''得到sqlite游标

        Args:       无
        Returns:
            cursor: 游标对象

        Raises:
            @exception_from: <sqlite3.Cursor>.execute
        '''
        return self.cursor.execute(statement)

    def commit(self):
        '''提交对Sqlite数据库的修改

        Args:       无
        Returns:
            sqlite3.Cursor: 游标对象

        Raises:
            @exception_from: <sqlite3.Connection>.commit
        '''
        return self.conn.commit()
    
    def get_type_name(self, field):
        '''得到基本类型在Sqlite数据库中的字符串表示

        Args:
            field: 基本字段类型
        Returns:
            str: 字段类型名字，见self.type_map

        Raises:     无
        '''
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
    
    def execute_end(self):
        return self.connHandle.commit()

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
        connection_context.execute_end()
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
def db_create_table(table_name, field_dict):
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
        connection_context.execute_end()
        return connection_context.get_cursor()
    except Exception as e:
        log_notice("create table failed: " + str(e))

@with_connection
def db_select(table_name_list, col_list='*', conditions=''):
    global connection_context

    if list == type(table_name_list):
        str_tables = ', '.join(table_name_list)
    else:
        str_tables = table_name_list

    if conditions:
        sql = "SELECT {} FROM {} WHERE ({})".format(
                col_list,
                str_tables,
                conditions,
            )
    else:
        sql = "SELECT {} FROM {}".format(col_list, str_tables)

    log_debug("execute sql(\"{}\")".format(sql))

    try:
        connection_context.execute(sql)
        return connection_context.get_cursor().fetchall()
    except Exception as e:
        log_notice("select records failed: " + str(e))

@with_connection
def db_insert(table_name, value_dict):
    global connection_context
    value_list = [e.__repr__() for e in value_dict.values()]
    name_list = value_dict.keys()

    sql = "INSERT INTO {} ({}) VALUES({})".format(
            table_name,
            ', '.join(name_list),
            ', '.join(value_list)
        )
    log_debug("execute sql(\"{}\")".format(sql))

    try:
        res = connection_context.execute(sql)
        return res
    except Exception as e:
        log_notice("insert record failed: " + str(e))

@with_connection
def db_delete(table_name, conditions=''):
    global connection_context
    if conditions:
        sql = "DELETE FROM {} WHERE ({})".format(
                table_name,
                conditions,
            )
    else:
        sql = "DELETE FROM {}".format(table_name)

    log_debug("execute sql(\"{}\")".format(sql))

    try:
        res =  connection_context.execute(sql)
        return res
    except Exception as e:
        log_notice("delete record failed: " + str(e))
