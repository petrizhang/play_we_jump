from random import randint
from adb_utils import *
from time import sleep


class JumpExecutor(object):
    @staticmethod
    def jump(swipe_time):
        x, y = randint(500, 1000), randint(300, 500)
        ret = adb_shell("input swipe {x} {y} {x} {y} {time}".format(x=x, y=y, time=swipe_time))
        if ret != 0:
            raise adb_error

    @staticmethod
    def sleep(seconds):
        sleep(seconds)
