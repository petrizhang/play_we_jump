import os
import subprocess

import cv2
import numpy as np
import matplotlib.pyplot as plt
from math import pi, tan
from random import randint
from time import sleep
import geometry_op as geo
from CVDrawer import CVDrawer


class WeJumpAgent(object):
    def __init__(self, android_img_path="/storage/emulated/0/WeJumpAgent.png",
                 local_img_path="./images/WeJumpAgent.png",
                 player_template_path="./images/player.png",
                 drawer=None):
        self.rotate_angle = -30

        self.android_img_path = android_img_path
        self.local_img_path = local_img_path
        self.player_template_path = player_template_path
        if drawer is None:
            self.drawer = CVDrawer()
        else:
            self.drawer = drawer
        self.raw_img = None  # 原始图像数据
        self.drawing_img = None  # 在此图上绘图
        self.edge_img = None  # 边缘检测得到的图像

        # 棋子矩形: ((top_left_x,top_left_y),(bottom_right_x,bottom_right_y))
        self.player_rec = ((None, None), (None, None))
        # 棋子位置: (center_x,center_y)
        self.player_point = (None, None)

        # 目标图形的顶点
        self.target_top_point = (None, None)
        # 根据tan(pi/6)算出来的目标位置
        self.tan_target_point = (None, None)

        # 目标矩形的两条线
        self.target_top_line = (None, None, None, None)
        self.target_bottom_line = (None, None, None, None)
        # 根据两条直线算出来的目标位置
        self.line_target_point = (None, None)

    @property
    def drawing_img_work_area(self):
        y_min, y_max = 500, 1200
        return self.drawing_img[y_min:y_max, :, :]

    @property
    def raw_img_work_area(self):
        y_min, y_max = 500, 1200
        return self.raw_img[y_min:y_max, :, :]

    def get_policy_path(self):
        # 必须按顺序执行
        self.get_player_pos()
        self.detect_edge()
        self.get_target_top_point()
        self.get_target_rec()

        self.get_tan_target_point()

    def detect_edge(self):
        raw = self.raw_img_work_area
        # 只使用一个通道检测
        # b, g, r = cv2.split(raw)
        # img = b
        img = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
        # 边缘检测
        threshold_low = 10
        self.edge_img = cv2.Canny(img, threshold_low, threshold_low * 3)
        # 将玩偶所在的竖直方向全部涂黑
        (top_left_x, top_left_y), (bottom_right_x, bottom_right_y) = self.player_rec
        # print((top_left_x, top_left_y), (bottom_right_x, bottom_right_y))
        self.edge_img[:, top_left_x:bottom_right_x] = 0

    def get_target_top_point(self):
        binary = self.edge_img
        index_y, index_x = np.where(binary != 0)

        first_y = index_y[0]
        for i in range(len(index_x)):
            now_y = index_y[i]
            if now_y != first_y:
                break
        self.target_top_point = geo.line_center((index_x[0], index_y[0], index_x[i - 1], index_y[i - 1]))

    def get_target_rec(self):
        binary = self.edge_img

        # TODO 防止检测不到直线
        # 直线检测
        lines = cv2.HoughLinesP(binary, 1, np.pi / 180, 30, minLineLength=60, maxLineGap=10)
        lines = lines[:, 0, :]  # 提取为二维
        # 计算斜率，取出范围在0.55~0.65之间的直线
        slopes = np.fromiter(map(lambda p: (p[3] - p[1]) / (p[2] - p[0]), lines), dtype=np.float32)
        lines = lines[np.logical_and(0.55 < slopes, slopes < 0.65)]
        # print(lines)
        # print(slopes)

        # 排序
        lines = np.asarray(sorted(lines, key=lambda x: x[1]))
        if lines.shape[0] == 0:
            print("---------------------error: line not detected.")
            return None

        bottom_line = None
        top_line = lines[0]
        x1, y1, x2, y2 = top_line
        top_line_length = geo.distance_point((x1, y1), (x2, y2))
        distance_square_threshold = (3 / 4 * top_line_length) ** 2
        for i in range(lines.shape[0]):
            bottom_line = lines[i]
            distance_square = geo.distance_square_point_line(geo.line_center(top_line), bottom_line)
            # print("distance_square:", distance_square)
            # print("threshold_square_threshold:", distance_square_threshold)
            if distance_square > distance_square_threshold:
                break
        if bottom_line is None:
            bottom_line = (x1, y1 + top_line_length, x2 - top_line_length, y2)

        top_left_x, top_left_y, top_right_x, top_right_y = top_line
        bottom_left_x, bottom_left_y, bottom_right_x, bottom_right_y = bottom_line

        rotate = lambda p: geo.axis_transform(self.rotate_angle, p)
        reverse_rotate = lambda p: geo.axis_transform(-self.rotate_angle, p)

        print("before rotate:")
        print("top_left:", top_left_x, top_left_y)
        print("top_right:", top_right_x, top_right_y)
        print("bottom_left:", bottom_left_x, bottom_left_y)
        print("bottom_right:", bottom_right_x, bottom_right_y)

        # 逆时针旋转30度
        top_left_x, top_left_y = rotate((top_left_x, top_left_y))
        top_right_x, top_right_y = rotate((top_right_x, top_right_y))
        bottom_left_x, bottom_left_y = rotate((bottom_left_x, bottom_left_y))
        bottom_right_x, bottom_right_y = rotate((bottom_right_x, bottom_right_y))

        min_left_x = min(top_left_x, bottom_left_x)
        max_right_x = max(top_right_x, bottom_right_x)

        top_y = max(top_left_y, top_right_y)
        bottom_y = min(bottom_left_y, bottom_right_y)

        print("after rotate:")
        print("top_left:", top_left_x, top_left_y)
        print("top_right:", top_right_x, top_right_y)
        print("bottom_left:", bottom_left_x, bottom_left_y)
        print("bottom_right:", bottom_right_x, bottom_right_y)

        top_left_x, top_left_y = reverse_rotate((min_left_x, top_y))
        top_right_x, top_right_y = reverse_rotate((max_right_x, top_y))
        bottom_left_x, bottom_left_y = reverse_rotate((min_left_x, bottom_y))
        bottom_right_x, bottom_right_y = reverse_rotate((max_right_x, bottom_y))

        top_line = tuple(map(geo.roundi, (top_left_x, top_left_y, top_right_x, top_right_y)))
        bottom_line = tuple(map(geo.roundi, (bottom_left_x, bottom_left_y, bottom_right_x, bottom_right_y)))

        self.draw_line(bottom_line)
        self.draw_line(top_line)

        center_x, center_y = geo.rec_center(bottom_line, top_line)

        self.draw_circle((center_x, center_y))

        return center_x, center_y

    def get_tan_target_point(self):
        start_x, start_y = self.player_point
        target_top_x, target_top_y = self.target_top_point
        end_x = target_top_x
        end_y = int(round(start_y - tan(pi / 6) * abs(target_top_x - start_x)))
        self.tan_target_point = (end_x, end_y)

        self.draw_circle(self.target_top_point)
        self.draw_circle(self.tan_target_point)
        self.draw_line_by_point(self.target_top_point, self.tan_target_point)
        self.draw_line_by_point(self.player_point, self.tan_target_point)

    def get_player_pos(self, method=cv2.TM_CCOEFF_NORMED):
        raw = self.raw_img_work_area
        img_gray = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
        img2 = img_gray.copy()

        template = cv2.imread(self.player_template_path, 0)
        w, h = template.shape[::-1]

        img = img2.copy()
        # Apply template Matching
        res = cv2.matchTemplate(img, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        # 画出位置
        center_x = round((bottom_right[0] + top_left[0]) / 2)
        center_y = bottom_right[1] - 30
        self.draw_circle((center_x, center_y))
        self.draw_rec(top_left, bottom_right)

        self.player_point = (center_x, center_y)
        self.player_rec = (top_left, bottom_right)

    def show_img(self):
        plt.subplot(211)
        plt.imshow(self._bgr2rgb(self.drawing_img))
        plt.subplot(212)
        plt.imshow(self.edge_img, cmap="gray")

    def save_img(self, img, img_prefix="problem"):
        img_name = "./image/{prefix}".format(prefix=img_prefix)
        i = 0
        while True:
            img_filename = "{img_name}{num}.png".format(img_name=img_name, num=i)
            if not os.path.exists(img_filename):
                break
            i += 1
        cv2.imwrite(img_filename, img)

    def _bgr2rgb(self, img):
        b, g, r = cv2.split(img)  # get b,g,r
        rgb_img = cv2.merge([r, g, b])  # switch it to rgb
        return rgb_img

    def draw_line_by_point(self, start, end, color=(0, 0, 255)):
        start_x, start_y = start
        end_x, end_y = end
        self.draw_line((start_x, start_y, end_x, end_y), color)

    def draw_line(self, line, color=(0, 0, 255)):
        self.drawer.draw_line(self.drawing_img_work_area, line, color)

    def draw_circle(self, center_point, color=(0, 0, 255)):
        self.drawer.draw_circle(self.drawing_img_work_area, center_point, color)

    def draw_rec(self, top_left, bottom_right, color=(0, 0, 255)):
        self.drawer.draw_rec(self.drawing_img_work_area, top_left, bottom_right, color)

    def adb_shell(self, cmd):
        adb_cmd = 'adb shell "{0}"'.format(cmd)
        self.shell(adb_cmd)

    def shell(self, cmd):
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print("-------------------- excuting shell command:")
        print(cmd)
        print()
        print("-------------------- result: ")
        for line in p.stdout.readlines():
            print(line.decode(), end="")
        print()
        retval = p.wait()

    def screenshot(self):
        self.adb_shell("screencap -p {0}".format(self.android_img_path))
        self.shell("adb pull {source} {target}".format(source=self.android_img_path, target=self.local_img_path))
        self.raw_img = cv2.imread(self.local_img_path)
        self.drawing_img = self.raw_img.copy()

    def jump(self, swipe_time):
        x, y = randint(500, 1000), randint(300, 500)
        self.adb_shell("input swipe {x} {y} {x} {y} {time}".format(x=x, y=y, time=swipe_time))

    def run(self):
        plt.ion()
        swipe_time = 0
        while True:
            sleep((swipe_time + 1000) / 1000)
            # capture screenshot
            self.screenshot()
            # 获取路线
            self.get_policy_path()

            # 保存图片
            # self.show_img()
            # plt.pause(0.01)
            cv2.imwrite("images/draw.png", self.drawing_img)
            cv2.imwrite("images/edge.png", self.edge_img)

            distance = geo.distance_point(self.player_point, self.tan_target_point)
            swipe_time = int(distance * 1.393)
            self.jump(swipe_time)


def main():
    a = WeJumpAgent()
    a.run()


# sleep((swipe_time+200) / 1000)

if __name__ == "__main__":
    main()
