class Drawer(object):
    def draw_line(self, img, line, color=(0, 0, 255)):
        raise NotImplementedError

    def draw_circle(self, img, center_point, color=(0, 0, 255)):
        raise NotImplementedError

    def draw_rec(self, img, top_left, bottom_right, color=(0, 0, 255)):
        raise NotImplementedError
