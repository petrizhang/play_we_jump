from Drawer import Drawer
import cv2


class CVDrawer(Drawer):
    def draw_line(self, img, line, color=(0, 0, 255)):
        x1, y1, x2, y2 = line
        cv2.line(img, (x1, y1), (x2, y2), color, 10)

    def draw_circle(self, img, center_point, color=(0, 0, 255)):
        center_x, center_y = center_point
        cv2.circle(img, (center_x, center_y), 10, color, -1)

    def draw_rec(self, img, top_left, bottom_right, color=(0, 0, 255)):
        cv2.rectangle(img, top_left, bottom_right, color, 10)
