from math import pi, tan
import cv2
import numpy as np

from GameAgent.InfoExtractor import InfoExtractor
from ImageProcessor import ImageProcessor
import geometry_op as geo


class JumpInfoExtractor(InfoExtractor):
    def __init__(self,
                 image_processor: ImageProcessor,
                 player_template_path="./images/player.png"):
        self.image_processor = image_processor
        self.raw_img = None  # 原始图像数据
        self.drawing_img = None  # 在此图上绘图
        self.edge_img = None  # 边缘检测得到的图像
        self.player_template_path = player_template_path

    def extract(self, known_info: dict) -> dict:
        img_path = known_info['img_path']
        self.raw_img = self.image_processor.imread(img_path)
        self.drawing_img = self.image_processor.imcopy(self.raw_img)
        xdistance = self.get_xdistance()
        return {'xdistance': xdistance,
                'drawing_img': self.drawing_img,
                'edge_img': self.edge_img}

    @property
    def drawing_img_work_area(self):
        y_min, y_max = 500, 1200
        return self.drawing_img[y_min:y_max, :, :]

    @property
    def raw_img_work_area(self):
        y_min, y_max = 500, 1200
        return self.raw_img[y_min:y_max, :, :]

    def get_xdistance(self, drawing=False):
        # 先获取棋子位置
        player_point, player_rec = self.get_player_pos()
        player_x, player_y = player_point
        # 进行边缘检测
        edge_img = self.detect_edge(player_rec)
        self.edge_img = edge_img
        # 检测目标顶点
        target_top_point_x, target_top_point_y = self.get_target_top_point(edge_img)

        if drawing:
            # 画出棋子所在位置

            self.draw_circle((player_x, player_y))
            # 画出棋子所在的矩形
            player_rec_top_left, player = player_rec
            self.draw_rec(player_rec_top_left, player)
            # 画出目标的最高点
            self.draw_circle((target_top_point_x, target_top_point_y))
            # 画出目标的两条边(如果检测到的话)

        return abs(player_x - target_top_point_x)

    def detect_edge(self, player_rec):
        raw = self.raw_img_work_area
        # 只使用一个通道检测
        # b, g, r = cv2.split(raw)
        # img = b
        img = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
        # 边缘检测
        threshold_low = 10
        edge_img = cv2.Canny(img, threshold_low, threshold_low * 3)
        # 将玩偶所在的竖直方向全部涂黑
        (top_left_x, top_left_y), (bottom_right_x, bottom_right_y) = player_rec
        # print((top_left_x, top_left_y), (bottom_right_x, bottom_right_y))
        edge_img[:, top_left_x:bottom_right_x] = 0
        return edge_img

    def get_player_pos(self, method=cv2.TM_CCOEFF_NORMED):
        """

        :param method:
        :return: player_point,player_rec
        """
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

        player_point = (center_x, center_y)
        player_rec = (top_left, bottom_right)

        return player_point, player_rec

    def get_target_top_point(self, edge_img):
        binary = edge_img
        index_y, index_x = np.where(binary != 0)

        first_y = index_y[0]
        for i in range(len(index_x)):
            now_y = index_y[i]
            if now_y != first_y:
                break
        target_top_point = geo.line_center((index_x[0], index_y[0], index_x[i - 1], index_y[i - 1]))
        return target_top_point

    def draw_line_by_point(self, start, end, color=(0, 0, 255)):
        start_x, start_y = start
        end_x, end_y = end
        self.draw_line((start_x, start_y, end_x, end_y), color)

    def draw_line(self, line, color=(0, 0, 255)):
        self.image_processor.draw_line(self.drawing_img_work_area, line, color)

    def draw_circle(self, center_point, color=(0, 255, 255)):
        self.image_processor.draw_circle(self.drawing_img_work_area, center_point, color)

    def draw_rec(self, top_left, bottom_right, color=(0, 0, 255)):
        self.image_processor.draw_rec(self.drawing_img_work_area, top_left, bottom_right, color)
