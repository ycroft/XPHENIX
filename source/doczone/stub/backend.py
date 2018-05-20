
from Cookie import SimpleCookie
import datetime

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
        'TYPE': 'normal',
        'VALUES': {
            'page_title': 'Welcome to Doczone !',
            'panel_title': panel_title,
            'panel_layout': panel_layout,
        }
    }

def handle_action_signup(args):
     
    expiration = datetime.datetime.now() + datetime.timedelta(days=30)

    cookies = SimpleCookie()
    cookies['session'] = 233
    cookies['session']['path'] = "/"
    cookies['session']['expires'] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")
    cookies['ban'] = 666
    cookies['ban']['path'] = "/"
    cookies['ban']['expires'] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")

    return {
        'TYPE': 'redirect',
        'PATH': '/admin/',
        'COOKIE': cookies,
    }

def handle_action_signin(args):
    return {
        'TYPE': 'redirect',
        'PATH': '/admin/',
    }

def handle_page_control_panel(args):
    return {
        'TYPE': 'normal',
        'VALUES': {
            'admin_name': 'Ycroft',
            'db_user_list': [
                    [1, 'userA', '111', 'Ada', '3345'],
                    [2, 'userB', '2', 'Bob', '3346'],
                    [3, 'userC', '3', 'Caros', '3347'],
                    [4, 'userD', '4', 'Dean', '3348'],
                    [5, 'userE', '5', 'Ella', '3349'],
                ],
        }
    } 

