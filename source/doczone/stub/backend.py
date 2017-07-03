
import hashlib
from doczone.mod.models import *

def handle_page_login(args):

    if not 'entry_type' in args:
        panel_title = 'DOC ZONE'
        panel_layout = 'signin'
    elif args['entry_type'] == 'signin':
        panel_title = 'DOC ZONE'
        panel_layout = 'signin'
    elif args['entry_type'] == 'signup':
        panel_title = 'DOC ZONE'
        panel_layout = 'signup'
    else:
        return None

    return {
            'page_title': 'Welcome to Doczone !',
            'panel_title': panel_title,
            'panel_layout': panel_layout,
        }

def handle_action_signup(args):
    user = User(
                login_name=args['user_name'],
                password=hashlib.md5(args['user_pwd']).hexdigest(),
                nick_name='YY',
                user_info='',
                last_login=0,
            )

    user.insert()
    pass

def handle_action_signin(args):
    pass

def handle_page_control_panel(args):
    result = {
            'admin_name': 'Ycroft',
            'db_user_list': [
                    [9527, 'fage', 'XXX', 'Mr. Fa', '', '0'],
                ],
        } 

    users = User.find_all(nick_name='YY')
    for u in users:
        result['db_user_list'].append([
                u['user_id'],
                u['login_name'],
                u['password'],
                u['nick_name'],
                u['user_info'],
                u['last_login'],
            ])

    return result

