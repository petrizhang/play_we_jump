from ImageProcessor import ImageProcessor
import cv2
import numpy as np
import matplotlib.pyplot as plt


class ImageProcessorCV(ImageProcessor):
    def __init__(self, player_template_path="./images/player.png"):
        self.player_template_path = player_template_path

    def imread(self, file_path: str):
        return cv2.imread(file_path)

    def imwrite(self, file_path: str, img: np.ndarray):
        return cv2.imwrite(file_path, img)

    def imcopy(self, img: np.ndarray):
        return img.copy()

    def draw_line(self, img, line, color=(0, 0, 255)):
        x1, y1, x2, y2 = line
        cv2.line(img, (x1, y1), (x2, y2), color, 10)

    def draw_circle(self, img, center_point, color=(0, 0, 255)):
        center_x, center_y = center_point
        cv2.circle(img, (center_x, center_y), 10, color, -1)

    def draw_rec(self, img, top_left, bottom_right, color=(0, 0, 255)):
        cv2.rectangle(img, top_left, bottom_right, color, 10)

    def save_img(self, img, img_prefix="problem"):
        img_name = "./image/{prefix}".format(prefix=img_prefix)
        i = 0
        while True:
            img_filename = "{img_name}{num}.png".format(img_name=img_name, num=i)
            if not os.path.exists(img_filename):
                break
            i += 1
        cv2.imwrite(img_filename, img)

