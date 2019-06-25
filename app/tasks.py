# coding = utf-8
"""
@author: zhou
@time:2019/6/25 16:47
"""

from threading import Timer
from .redis_conn import redis_conn_pool
import time


r = redis_conn_pool()


class Scheduler(object):
    def __init__(self, sleep_time, func, mytime=None):
        self.sleep_time = sleep_time
        self.func = func
        self._t = None
        self.mytime = mytime

    def start(self):
        if self._t is None:
            self._t = Timer(self.sleep_time, self._run)
            self._t.start()
        else:
            raise Exception("this timer is already running")

    def _run(self):
        if self.mytime is not None:
            self.func(self.mytime)
        else:
            self.func()
        self._t = Timer(self.sleep_time, self._run)
        self._t.start()

    def stop(self):
        if self._t is not None:
            self._t.cancel()
            self._t = None

    @staticmethod
    def init_app(app):
        pass


def keep_msg(mytime=None):
    if mytime is not None:
        expare_time = mytime
    else:
        expare_time = 604800
    msg_list = r.keys("msg-*")
    for msg in msg_list:
        _ = r.zrange(msg, 0, 0)
        for i in _:
            score = r.zscore(msg, i)
            if time.time() - score > expare_time:
                r.zrem(msg, i)
                # print("success del key from redis")
