# coding = utf-8
from datetime import datetime

import threading

is_allowed = {
    'EMERGENCY': True,
    'ERROR': True,
    'WARNING': True,
	'NOTICE': True,
    'DEBUG': True,
}

def CONSOLE(ctx):
    print(ctx)

def _format_log(level, msg):
    thread = threading.current_thread()
    return "[{}][PID|{}][{}]{}".format(
            datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
            thread.getName(),
            level,
            msg
        )

def log_out(ctx):
    CONSOLE(ctx)

def _log_in_level(level, msg):
    if not level in is_allowed:
        return
    log_context = _format_log(level, msg)
    if is_allowed[level]:
        log_out(log_context)

def log_emergency(msg):
    _log_in_level('EMERGENCY', msg)

def log_error(msg):
    _log_in_level('ERROR', msg)

def log_warning(msg):
    _log_in_level('WARNING', msg)

def log_notice(msg):
    _log_in_level('NOTICE', msg)

def log_debug(msg):
    _log_in_level('DEBUG', msg)
