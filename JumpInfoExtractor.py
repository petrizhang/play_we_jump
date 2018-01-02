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
        distance = self.get_distance()
        return {'distance': distance,
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

    def get_distance(self, drawing=False):
        # 先获取棋子位置
        player_point, player_rec = self.get_player_pos()

        # 进行边缘检测
        edge_img = self.detect_edge(player_rec)
        self.edge_img = edge_img
        # 检测目标顶点
        target_top_point_x, target_top_point_y = self.get_target_top_point(edge_img)
        target_point_approximate = (target_top_point_x, target_top_point_y + 30)

        # # 检测目标两条边
        # top_line, bottom_line = self.get_target_line(edge_img)
        #
        # # 如果检测到目标矩形
        # if top_line is not None:
        #     top_line, bottom_line = self.fit_line(top_line, bottom_line)
        #     line_center_point = geo.rec_center(bottom_line, top_line)
        #     # 确实检测到了目标矩形而不是其他的矩形
        #     if geo.in_area(target_point_approximate, top_line, bottom_line) and geo.distance_point(
        #             target_point_approximate, line_center_point) < 150:
        #         # target_point = line_center_point
        #         k, b = geo.kb_of_line(bottom_line)
        #         target_point = (target_top_point_x,
        #                         geo.roundi((target_top_point_y + k * target_top_point_x + b) / 2))
        #     else:
        #         target_point = target_point_approximate
        # else:
        #     target_point = target_point_approximate

        target_point = self.get_tan_target_point(player_point, (target_top_point_x, target_top_point_y))
        if drawing:
            # 画出棋子所在位置
            target_line_center_x, target_line_center_y = player_point
            self.draw_circle((target_line_center_x, target_line_center_y))
            # 画出棋子所在的矩形
            player_rec_top_left, plater_rec_bottom_right = player_rec
            self.draw_rec(player_rec_top_left, plater_rec_bottom_right)
            # 画出目标的最高点
            self.draw_circle((target_top_point_x, target_top_point_y))
            # 画出目标的两条边(如果检测到的话)
            if top_line is not None:
                self.draw_line(top_line)
                self.draw_line(bottom_line)
                self.draw_circle((target_line_center_x, target_line_center_y))
            self.draw_circle(target_point)
            self.draw_line_by_point(player_point, target_point)

        return geo.distance_point(player_point, target_point)

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

    def get_target_line(self, edge_img):
        """
        获取目标棋盘的两条边（如果是矩形的话）

        :return: 检测成功返回(top_line, bottom_right)
                  也即((x1,y1,x2,y2),(x3,y3,x4,y4))
                  检测失败（目标棋盘是圆形的情况）返回None
        """
        binary = edge_img

        # 直线检测
        lines = cv2.HoughLinesP(binary, 1, np.pi / 180, 30, minLineLength=60, maxLineGap=10)
        lines = lines[:, 0, :]  # 提取为二维
        # 计算斜率，取出范围在0.55~0.65之间的直线
        slopes = np.fromiter(map(lambda p: (p[3] - p[1]) / (p[2] - p[0]), lines), dtype=np.float32)
        lines = lines[np.logical_and(0.55 < slopes, slopes < 0.65)]

        # 排序
        lines = np.asarray(sorted(lines, key=lambda x: x[1]))
        if lines.shape[0] == 0:
            print("---------------------warning: line not detected.")
            return None, None

        bottom_line = None
        top_line = lines[0]
        x1, y1, x2, y2 = top_line
        top_line_length = geo.distance_point((x1, y1), (x2, y2))
        distance_square_threshold = (3 / 4 * top_line_length) ** 2
        for i in range(lines.shape[0]):
            bottom_line = lines[i]
            distance_square = geo.distance_square_point_line(geo.line_center(top_line), bottom_line)
            if distance_square > distance_square_threshold:
                break
        if bottom_line is None:
            bottom_line = (x1, y1 + top_line_length, x2 - top_line_length, y2)

        return top_line, bottom_line

    def fit_line(self, top_line, bottom_line):
        """
        把两条线改成覆盖面积最大的形式，也就是把较短的线按照两直线平行方向拉长
        :param top_line:
        :param bottom_line:
        :return:
        """
        top_left_x, top_left_y, top_right_x, top_right_y = top_line
        bottom_left_x, bottom_left_y, bottom_right_x, bottom_right_y = bottom_line

        # 左上角到上方直线引直线的交点
        joint_x, joint_y = geo.joint((bottom_left_x, bottom_left_y),
                                     (top_left_x, top_left_y, top_right_x, top_right_y))
        if joint_x < top_left_x:
            top_left_x, top_left_y = joint_x, joint_y
        else:
            # 右上角到下方直线引直线的交点
            joint_x, joint_y = geo.joint((top_left_x, top_left_y),
                                         (bottom_left_x, bottom_left_y, bottom_right_x, bottom_right_y))
            bottom_left_x, bottom_left_y = joint_x, joint_y
        # 左下角到上方直线引直线的交点
        joint_x, joint_y = geo.joint((bottom_right_x, bottom_right_y),
                                     (top_left_x, top_left_y, top_right_x, top_right_y))
        if joint_x > top_right_x:
            top_right_x, top_right_y = joint_x, joint_y
        else:
            # 右下角到下方直线引直线的交点
            joint_x, joint_y = geo.joint((top_right_x, top_right_y),
                                         (bottom_left_x, bottom_left_y, bottom_right_x, bottom_right_y))
            bottom_right_x, bottom_right_y = joint_x, joint_y

        top_line = tuple(map(geo.roundi, (top_left_x, top_left_y, top_right_x, top_right_y)))
        bottom_line = tuple(map(geo.roundi, (bottom_left_x, bottom_left_y, bottom_right_x, bottom_right_y)))

        return top_line, bottom_line

    def get_tan_target_point(self, player_point, target_top_point):
        start_x, start_y = player_point
        target_top_x, target_top_y = target_top_point
        end_x = target_top_x
        end_y = int(round(start_y - tan(pi / 6) * abs(target_top_x - start_x)))
        tan_target_point = (end_x, end_y)
        return tan_target_point

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
