from math import sqrt, sin, cos, pi
import numpy as np


def line_len(line):
    return (line[2] - line[0]) ** 2 + (line[3] - line[1]) ** 2


def line_center(line):
    x1, y1, x2, y2 = line
    return int(round((x1 + x2) / 2)), int(round((y1 + y2) / 2))


def rec_center(line1, line2):
    x1, y1 = line_center(line1)
    x2, y2 = line_center(line2)
    return int(round((x1 + x2) / 2)), int(round((y1 + y2) / 2))


def distance_square_point_line(point, line):
    """
    点到线段的距离平方和
    """
    x, y = point
    x1, y1, x2, y2 = line
    A = (y2 - y1) / (x2 - x1)
    B = -1
    C = y1 - x1 * (y2 - y1) / (x2 - x1)
    return (A * x + B * y + C) ** 2 / (A * A + B * B)


def distance_point(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)


def is_point_in_lines(point, line1, line2):
    x, y = point
    lx1, ly1, lx2, ly2 = line1
    rx1, ry1, rx2, ry2 = line2


def kb_of_line(p1, p2):
    """
    根据两点求直线斜率和截距
    """
    x1, y1 = p1
    x2, y2 = p2
    k = (y2 - y1) / (x2 - x1)
    b = y1 - k * x1
    return k, b


def line_joint(k1, b1, k2, b2):
    """
    由斜率和截距求两直线交点
    """
    # y = k1*x + b1
    # y = k2*x + b2
    # -k1*x + y = b1
    # -k2*x + y = b2
    left = [[k1, 1],
            [k2, 1]]
    right = [[b1], [b2]]
    return tuple(np.linalg.solve(left, right)[:, 0])


def roundi(num):
    return int(round(num))
