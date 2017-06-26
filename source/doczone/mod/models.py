
from ant.commom.orm import Model

MAX_UINT8 = 0xFF
MAX_UINT16 = 0xFFFF
MAX_UINT32 = 0xFFFFFFFF
MAX_UINT64 = 0xFFFFFFFFFFFFFFFF

class User(Model):
    user_id = NumberField(size=MAX_UINT32, is_pk=True)
    login_name = StringField(len=255)
    password = StringField(len=32)
    nick_name = StringField(len=255)
    user_info = StirngField(len=1024)
    last_login = NumberField(size=MAX_UINT64)

