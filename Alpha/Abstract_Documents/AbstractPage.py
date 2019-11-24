# from Abstract_Documents.AbstractPage import AbstractPage
from Segment import Segment
from PointVector import Point
from C_implementation import get_pass_corners
from PIL import Image
import pytesseract
import numpy
import math
import os
import cv2 as cv


class AbstractPage:
    def __init__(self, path: str, deletion_key=True, analysis_key=True):
        self.deletion_key = deletion_key
        self.analysis_key = analysis_key
        self.path = path
        self.fields = []
        if self.analysis_key:
            self.LETS_ROLL()

    def __del__(self):
        if(self.deletion_key):
            os.system("rm " + self.path)

    def add_field(self, field):
        self.fields.append(field)

    def get_text_from_page(self):
        text = {}
        for field in self.fields:
            text[field['name']] = self.get_text_form_field(field)
        return text

    def percentage_crop(self, image, upper_left, lower_right, params={}):
        upper_left = Point(upper_left.x * image.size[1], upper_left.y * image.size[0])
        lower_right = Point(lower_right.x * image.size[1], lower_right.y * image.size[0])
        return AbstractPage.prepare_image_part(image, upper_left, lower_right,
                                               canvas_size=(params["canvas_size"] if "canvas size" in params else None),
                                               color=(params["color"] if "color" in params else None),
                                               brightness_border=(params["brightness_border"] if "brightness_border" in params else None))

    def get_text_form_field(self, field):
        upper_left = Point(field["coords"][1], field["coords"][0])
        lower_right = Point(field["coords"][3], field["coords"][2])
        image = self.percentage_crop(self.get_image(), upper_left, lower_right, field['params'])
        return pytesseract.image_to_string(image, lang=field['lang'])


    def save_image(self, path=None, image=None):
        if path is None:
            path = self.path
            # path = "./images/jopa.jpg"
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
        if brightness_border is None:
            brightness_border = 180
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
        image = AbstractPage.crop(image, upper_left, lower_right)
        if make_bw:
            image = AbstractPage.give_bw(image, brightness_border)
        if do_fill:
            image = AbstractPage.fill_around(image, canvas_size=canvas_size, center=center, color=color)
        return image

    @staticmethod
    def get_all_working_parameters(path_to_image, coords, answer, lang=None):
        if lang is None:
            lang_list = ["eng"]
        else:
            lang_list = [lang]
        upper_left = [coords[0], coords[1]]
        lower_right = [coords[2], coords[3]]
        height = coords[2] - coords[0]
        width = coords[3] - coords[1]
        image = Image.open(path_to_image)
        canvas_size_list = [[x * height, x * width] for x in numpy.arange(1, 5, 0.2)]
        color_list = ["white", "black"]
        brightness_border_list = range(130, 220, 5)
        ret = []
        for lang in lang_list:
            for canvas_size in canvas_size_list:
                for color in color_list:
                    for brightness_border in brightness_border_list:
                        piece_of_image = AbstractPage.prepare_image_part(image, upper_left=upper_left, lower_right=lower_right,
                                                                     canvas_size=canvas_size, color=color, brightness_border=brightness_border)
                        if answer == pytesseract.image_to_string(piece_of_image, lang=lang):
                            ret.append({"lang": lang, "canvas_size": canvas_size, "color": color,
                                        "brightness_border": brightness_border})

    @staticmethod
    def validate(upper_left, lower_right, max_size):
        ret = True
        return 0 <= upper_left.x < lower_right.x <= max_size[0] and 0 <= upper_left.y < lower_right.y <= max_size[1]

    def get_image_part(self, upper_left, lower_right, canvas_size=None, center=None,
                       color="white", brightness_border=180):
        return AbstractPage.prepare_image_part(image=self.get_image(), upper_left=upper_left, lower_right=lower_right,
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

    def get_edges(self, arg1=7, arg2=14):
        edges = self.get_image().convert('L')
        edges = numpy.array(edges)
        edges = cv.Canny(edges, arg1, 14)
        return edges

    def get_mini_edges(self, shrinking=4, arg1=16, arg2=14):
        edges = self.get_image().convert('L')
        print(edges.size)
        edges.thumbnail([x/shrinking for x in edges.size], Image.ANTIALIAS)
        print(edges.size)
        edges = numpy.array(edges)
        edges = cv.Canny(edges, arg1, 32)
        print(edges.size)
        return edges

    # def cleaner(self):
    #     os.system("rm new_C_directory/image.txt")
    #     os.system("rm new_C_directory/coordinates_4p.txt")

    def LETS_ROLL(self):
        shrinking = 8
        edges = self.get_mini_edges(shrinking=shrinking)
        # fucking debug starts
        # with open("new_C_directory/image.txt", "w") as f:
        #     a = edges.tolist()
        #     f.write(str(len(a)) + ' ' + str(len(a[0])))
        #     for i in a:
        #         for j in i:
        #             f.write(' ' + str(j))
        # fucking debug ends
        # start of cpp block
        coords = get_pass_corners(edges)
        print(coords)
        coords = [x*shrinking for x in coords]
        print(coords)
        # end of cpp block
        # There are x and y swap because array looks like [x, y] but Image looks like [y, x]
        diag1 = Segment(Point(coords[1], coords[0]), Point(coords[3], coords[2]))
        diag2 = Segment(Point(coords[5], coords[4]), Point(coords[7], coords[6]))
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
        image = image.rotate(angle * 180 / math.pi)
        diag1.rotate(-angle, center)
        diag2.rotate(-angle, center)
        upper_left = Point((diag1.get_min_x() + diag2.get_min_x()) // 2,
                           (diag1.get_min_y() + diag2.get_min_y()) // 2)
        lower_right = Point((diag1.get_max_x() + diag2.get_max_x()) // 2,
                            (diag1.get_max_y() + diag2.get_max_y()) // 2)
        image = self.crop(image, upper_left, lower_right)
        print("before save")
        self.save_image(image=image)
