
from ant.common.dbapi import NumberField
from ant.common.dbapi import StringField
from ant.common.orm import Model

MAX_UINT8 = 0xFF
MAX_UINT16 = 0xFFFF
MAX_UINT32 = 0xFFFFFFFF
MAX_UINT64 = 0xFFFFFFFFFFFFFFFF

class USER_PRIVILAGE:
    ADMIN = 0
    NORMAL = 1
    

class User(Model):
    user_id = NumberField(size=MAX_UINT32, is_pk=True)
    login_name = StringField(len=255)
    password = StringField(len=32)
    nick_name = StringField(len=255)
    user_info = StringField(len=1024)
    last_login = NumberField(size=MAX_UINT64)

class Column(Model):
    col_id = NumberField(size=MAX_UINT32, is_pk=True)
    parent = NumberField(size=MAX_UINT32)

class Project(Model):
    proj_id = NumberField(size=MAX_UINT32, is_pk=True)
    col_id = NumberField(size=MAX_UINT32)
    owner_id = NumberField(size=MAX_UINT32)
    title = StringField(len=1024)
    description = TextField()
    root_path = StringField(len=4096)

class File(Model):
    file_id = NumberField(size=MAX_UINT32, is_pk=True)
    proj_id = NumberField(size=MAX_UINT32)
    privilage = NumberField(size=MAX_UINT8)
    file_name = StringField(len=1024)
    path = StringField(len=4096)

MODEL_LIST = [User, Column, Project, File]

