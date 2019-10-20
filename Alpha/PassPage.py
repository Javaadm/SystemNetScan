from Alpha.Segment import Segment
from Alpha.PointVector import Point
from PIL import Image
import numpy
import math
import os
import cv2 as cv


class PassPage:
    def __init__(self, path: str, deletion_key=True, analysis_key=True):
        self.deletion_key = deletion_key
        self.analysis_key = analysis_key
        self.path = path
        if self.analysis_key:
            self.LETS_ROLL()

    def __del__(self):
        if(self.deletion_key):
            os.system("rm " + self.path)

    def save_image(self, path=None, image=None):
        if path is None:
            path = self.path
        if image is None:
            Image.open(self.path).save(path)
        else:
            image.save(path)


    def get_image(self):
        return Image.open(self.path)

    def upside_down(self):
        self.get_image().rotate(180).save(self.path)
        return self

    @staticmethod
    def crop(image, upper_left, lower_right):
        return image.crop([upper_left.y, upper_left.x, lower_right.y, lower_right.x])

    @staticmethod
    def give_bw(image, brightness_border=180):
        column = image
        gray = column.convert('L')
        bw_image = gray.point(lambda x: 0 if x < brightness_border else 255, '1')
        return bw_image

    @staticmethod
    def fill_around(image, canvas_size=None, center=None, color="white"):
        if center is None:
            center = Point(image.size[0]//2, image.size[1]//2)
        if canvas_size is None:
            canvas_size = [3*x for x in image.size]
        canvas = Image.new("RGB", canvas_size, color)
        canvas.paste(image, (canvas_size[0] // 2 - center.x, canvas_size[1] // 2 - center.y))
        return canvas

    @staticmethod
    def prepare_image_part(image, upper_left, lower_right, canvas_size=None, center=None,
                           color="white", brightness_border=180, make_bw=True, do_fill=True):
        image = PassPage.crop(image, upper_left, lower_right)
        if make_bw:
            image = PassPage.give_bw(image, brightness_border)
        if do_fill:
            image = PassPage.fill_around(image, canvas_size=canvas_size, center=center, color=color)
        return image

    def get_image_part(self, upper_left, lower_right, canvas_size=None, center=None,
                       color="white", brightness_border=180):
        return PassPage.prepare_image_part(image=self.get_image(), upper_left=upper_left, lower_right=lower_right,
                                       canvas_size=canvas_size, center=center, color=color,
                                       brightness_border=brightness_border)

    def fill_and_give_points(self, image, diag1, diag2, canvas_size, center=None, color="white"):
        if center is None:
            center = Point(image.size[0] // 2, image.size[1] // 2)
        ret_image = self.fill_around(image, canvas_size, center, color)
        new_start = Point(canvas_size[0]//2 - center.x, canvas_size[1]//2 - center.y)
        diag1.make_shift(new_start)
        diag2.make_shift(new_start)
        return ret_image, diag1, diag2

    def get_edges(self):
        edges = self.get_image().convert('L')
        edges = numpy.array(edges)
        edges = cv.Canny(edges, 7, 14)
        return edges

    def cpp_launcher(self):
        os.system("./C_directory/get_pass_corners")

    def cleaner(self):
        os.system("rm C_directory/image.txt")
        os.system("rm C_directory/coordinates_4p.txt")

    def LETS_ROLL(self):
       edges = self.get_edges()
       with open("C_directory/image.txt", "w") as f:
           a = edges.tolist()
           f.write(str(len(a)) + ' ' + str(len(a[0])))
           for i in a:
               for j in i:
                   f.write(' ' + str(j))
       # start of cpp block
       self.cpp_launcher()
       # end of cpp block
       coords = []
       with open("C_directory/coordinates_4p.txt", "r+") as file:
           arr = file.readline().split(' ')
           coords = [int(x) for x in (arr)]
       diag1 = Segment(Point(coords[0], coords[1]), Point(coords[2], coords[3]))
       diag2 = Segment(Point(coords[4], coords[5]), Point(coords[6], coords[7]))
       center = Segment(diag1.get_center(), diag2.get_center()).get_center()
       center.round()
       image, diag1, diag2 = \
           self.fill_and_give_points(self.get_image(),
                                     diag1, diag2, (int(diag1.get_length()), int(diag1.get_length())), center)
       side1 = Segment(diag1.start, diag2.start)
       side2 = Segment(diag1.start, diag2.end)
       if side1.get_length() < side2.get_length():
           angle = side2.get_polar_angle()
       else:
           angle = side1.get_polar_angle()
       image = image.rotate(angle*180/math.pi)
       diag1.rotate(-angle, center)
       diag2.rotate(-angle, center)
       upper_left = Point((diag1.get_min_x() + diag2.get_min_x())//2,
                           (diag1.get_min_y() + diag2.get_min_y())//2)
       lower_right = Point((diag1.get_max_x() + diag2.get_max_x())//2,
                           (diag1.get_max_y() + diag2.get_max_y())//2)
       image = self.crop(image, upper_left, lower_right)
       self.save_image(image=image)
       self.cleaner()

