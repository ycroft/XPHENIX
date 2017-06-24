
from multiprocessing import Process
import os
import signal
import threading
import time

from ant.common.log import *

MONITOR_WATCH_INTVAL = 1    # 1 second
MONITOR_BOOT_INTVAL = 5     # 5 second

class Task(object):

    def __init__(self):
        pass
    
    def task_start(self, *args, **kwargs):
        pass
    
    def ask_self(self):
        return True

class Monitor(object):
    
    def __init__(self, task):
        self.task = task
        self.always_ask = True
        self.always_reboot = True
        self.watch_pid = 0

    def start_and_watch(self):
        
        while self.always_reboot:

            try:
                p = Process(target=self.task.task_start)
                p.start()
                self.watch_pid = p.pid
            except Exception as e:
                log_emergency('boot fail:{}'.format(str(e)))
                log_notice('try to reboot...')

            self.always_ask = True

            while self.always_ask:

                time.sleep(MONITOR_WATCH_INTVAL)
                
                if not self.task.ask_self():

                    log_emergency('ask pid({}) with no response. try to kill...'.format(
                            self.watch_pid
                        ))

                    os.kill(self.watch_pid, signal.SIGKILL)
                    self.always_ask = False
                    break
                
                pass
                
            time.sleep(MONITOR_BOOT_INTVAL)
