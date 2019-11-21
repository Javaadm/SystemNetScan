from PointVector import Point
import math


class Segment:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    def get_length(self):
        return math.sqrt((self.start.x - self.end.x)**2
                         + (self.start.y - self.end.y)**2)

    def get_center(self):
        return Point((self.start.x + self.end.x)/2,
                     (self.start.y + self.end.y)/2)

    def round(self):
        self.start.round()
        self.end.round()

    def get_polar_angle(self):
        return Point(self.end.x - self.start.x,
                     self.end.y - self.start.y).get_polar_angle()

    def rotate(self, rotation_angle, center=Point(0, 0)):
        self.start.rotate(rotation_angle, center)
        self.end.rotate(rotation_angle, center)

    def make_shift(self, new_start):
        self.start.x += new_start.x
        self.start.y += new_start.y
        self.end.x += new_start.x
        self.end.y += new_start.y

    def get_min_x(self):
        if (self.start.x > self.end.x):
            return self.end.x
        else:
            return self.start.x

    def get_max_x(self):
        if (self.start.x < self.end.x):
            return self.end.x
        else:
            return self.start.x

    def get_min_y(self):
        if (self.start.y > self.end.y):
            return self.end.y
        else:
            return self.start.y

    def get_max_y(self):
        if (self.start.y < self.end.y):
            return self.end.y
        else:
            return self.start.y
