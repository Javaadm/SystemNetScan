from Alpha.Segment import Segment
from Alpha.PointVector import Point
from PIL import Image
import math
import cv2 as cv


class Pass:

    def __init__(self, path: str):
        self.image = Image.open(path)
        self.path = path

    def __init__(self, image):
        self.image = image

    def crop(self, image, upper_left, lower_right):
        return image.crop(upper_left.y, upper_left.x, lower_right.y, lower_right.x)

    def give_bw(self, image, brightness_border=180):
        column = image
        gray = column.convert('L')
        bw_image = gray.point(lambda x: 0 if x < brightness_border else 255, '1')
        return bw_image

   def fill_around(self, image, canvas_size, center=None, color="white"):
        if center is None:
            center = Point(image.size()[1]//2, image.size()[0]//2)
        canvas = Image.new("RGB", canvas_size, color)
        canvas.paste(image, (canvas_size[0] // 2 - center.y, canvas_size[1] // 2 - center.x))
        return canvas

    def fill_and_give_points(self, diag1, diag2, image, canvas_size, center=None, color="white"):
        if center is None:
            center = Point(image.size()[1] // 2, image.size()[0] // 2)
        ret_image = self.fill_around(image,canvas_size, center, color)
        new_start = Point(canvas_size//2 - center.x, canvas_size//2 - center.y)
        diag1.make_shift(new_start)
        diag2.make_shift(new_start)
        return ret_image, diag1, diag2


    def get_edges(self):
        edges = self.image.convert('L')
        edges = cv.Canny(edges, 7, 14)
        pil_image = Image.fromarray(edges)
        return pil_image

    # This guy will be __init__ in the future
    def LETS_ROLL(self):
        self.edges = self.get_edges()
        with open("C_directory/image.txt", "w") as f:
            a = self.edges.tolist()
            f.write(str(len(a)) + ' ' + str(len(a[0])))
            for i in a:
                for j in i:
                    f.write(' ' + str(j))
        # start of cpp block

        # end of cpp block
        coords = []
        with open("C_directory/coordinates_4p.txt", "r+") as file:
            arr = file.readline().split(' ')
            coords = [int(x) for x in (arr)]
        diag1 = Segment(coords[0], coords[1], coords[2], coords[3])
        diag2 = Segment(coords[4], coords[5], coords[6], coords[7])
        center = Segment(diag1.get_center(), diag2.get_center()).get_center()
        self.image, diag1, diag2 = \
            self.fill_and_give_points(self.image,
                                      diag1, diag2, int(diag1.get_length()), center)
        side1 = Segment(diag1.start, diag2.start)
        side2 = Segment(diag1.start, diag2.end)
        if side1.get_length() > side2.get_length():
            angle = side2.get_polar_angle()
        else:
            angle = side1.get_polar_angle()
        self.image = self.image.rotate(-angle*180/math.pi)
        diag1.rotate(-angle, center)
        diag2.rotate(-angle, center)
        upper_left = Point((diag1.get_min_x() + diag2.get_min_x())//2,
                            (diag1.get_min_y() + diag2.get_min_y())//2)
        lower_right = Point((diag1.get_max_x() + diag2.get_max_x())//2,
                            (diag1.get_max_y() + diag2.get_max_y())//2)
        self.image = self.crop(self.image, upper_left, lower_right)






