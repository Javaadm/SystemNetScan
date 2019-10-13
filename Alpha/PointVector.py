import math


class Point:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def get_center(self, start, end):
        self.x = end.x - start.x
        self.y = end.y - start.y

    def get_rotated(self, rad_angle, origin=None):
        if origin is None:
            origin = Point(0, 0)
        new_x = origin.x + math.cos(rad_angle) * (self.x - origin.x) - math.sin(rad_angle) * (self.y - origin.y)
        new_y = origin.y + math.sin(rad_angle) * (self.x - origin.x) + math.cos(rad_angle) * (self.y - origin.y)
        return Point(new_x, new_y)

    def rotate(self, rad_angle, origin=None):
        self = self.get_rotated(rad_angle, origin=origin)

    def round(self):
        self.x = int(self.x)
        self.y = int(self.y)

    def get_polar_angle(self):
        return -(math.atan2(self.x, self.y))
