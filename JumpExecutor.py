from random import randint
from adb_utils import *
from time import sleep
import matplotlib.pyplot as plt
import cv2


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

    @staticmethod
    def show(drawing_img, edge_img):
        return

        def _bgr2rgb(img):
            b, g, r = cv2.split(img)  # get b,g,r
            rgb_img = cv2.merge([r, g, b])  # switch it to rgb
            return rgb_img

        plt.subplot(211)
        plt.imshow(_bgr2rgb(drawing_img))
        plt.subplot(212)
        plt.imshow(edge_img, cmap="gray")

        plt.pause(0.01)
