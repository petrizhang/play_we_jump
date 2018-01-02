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


def kb_of_line(line):
    """
    根据两点求直线斜率和截距
    """
    x1, y1, x2, y2 = line
    k = (y2 - y1) / (x2 - x1)
    b = y1 - k * x1
    return k, b


def line_joint(k1, b1, k2, b2):
    """
    由斜率和截距求两直线交点
    :param k1: 直线1斜率
    :param b1: 直线1截距
    :param k2: 直线2斜率
    :param b2: 直线2截距
    :return: 交点坐标(x,y), tuple
    """
    # y = k1*x + b1
    # y = k2*x + b2
    # -k1*x + y = b1
    # -k2*x + y = b2
    left = [[-k1, 1],
            [-k2, 1]]
    right = [[b1], [b2]]
    return tuple(np.linalg.solve(left, right)[:, 0])


def joint(point, line):
    """
    过一点引30度斜线与另一条线的交点
    :param point: 点 (x,y)
    :param line: (x1,y1,x2,y2)
    :return:
    """
    # 两条直线的斜率和截距
    x, y = point

    # 求线的斜率和截距
    k, b = kb_of_line(line)

    # 过点(x,y)，与x轴夹角30度直线的斜率和截距
    k0 = -sqrt(3) / 3
    b0 = y - k0 * x
    return line_joint(k, b, k0, b0)


def in_area(point, line1, line2):
    """
    近似的判断point是否在两线构成的多边形内
    :param point:
    :param line1:
    :param line2:
    :return:
    """
    lx1, ly1, lx2, ly2 = line1
    rx1, ry1, rx2, ry2 = line2
    xlist = (lx1, lx2, rx1, rx2)
    ylist = (ly1, ly2, ry1, ry2)
    minx = min(xlist)
    maxx = max(xlist)
    miny = min(ylist)
    maxy = max(ylist)
    x, y = point
    return minx < x < maxx and miny < y < maxy


def line_from_points(point1, point2):
    x1, y1 = ponit1
    x2, y2 = point2
    return (x1, y1, x2, y2)


def roundi(num):
    return int(round(num))
