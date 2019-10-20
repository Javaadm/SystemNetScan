from PIL import Image, ImageDraw, ImageFont
from pdf2image import convert_from_path
import pytesseract
import tesserocr
from PIL import Image
import json
from Alpha.PassPage import PassPage
from Alpha.PointVector import Point
from Alpha.Pass import Pass


class UkrPass(Pass):
    def __init__(self, path_to_pdf, path_to_images, deletion_key=True, analysis_key=True, debugging=False):
        super().__init__(path_to_pdf=path_to_pdf, path_to_images=path_to_images, deletion_key=deletion_key,
                         analysis_key=analysis_key, debugging=debugging)

    def arrange_pages(self):
        new_list = (self.find_pages(["passport"]))
        self.pages = [new_list[key] for key in sorted(new_list.keys())]

    def clear(self):
        pass

    def get_fields(self):
        second_page = self.get_second_page_text()
        pass_info = second_page
        return pass_info

    def prepare_json(self):
        pass

    def cut_page_number(self, page):
        crop = [x for x in page.get_image().size] * 2
        crop[0] = 0.151*crop[0]
        crop[1] = 0.581*crop[1]
        crop[2] = 0.29*crop[2]
        crop[3] = 0.601*crop[3]
        image = page.get_image_part(Point(crop[1], crop[0]), Point(crop[3], crop[2]),
                                    brightness_border=150)
        # image.save(page.path[:-4] + "number" + ang + ".jpg")
        return image

    def get_second_page_text(self):
        second_page_text = dict()
        second_page_image = self.pages[0].get_image()
        second_page_text["first_name"] = self.first_name(second_page_image)
        second_page_text["surname"] = self.surname(second_page_image)
        second_page_text["patronymic"] = self.patronymic(second_page_image)
        # second_page_text["birth_date"] = self.birth_date(second_page_image)
        # second_page_text["birth_place"] = self.birth_place(second_page_image)
        # second_page_text["personal_number"] = self.personal_number(second_page_image)
        # second_page_text["issuing_date"] = self.issuing_date(second_page_image)
        # second_page_text["expiration_date"] = self.expiration_date(second_page_image)
        return second_page_text

    def get_sixteen_page_text(self):
        pass

    def first_name(self, image):
        upper_left = Point(0.621 * image.size[1], 0.199 * image.size[0])
        lower_right = Point(0.654 * image.size[1], 0.324 * image.size[0])
        image = PassPage.prepare_image_part(image, upper_left, lower_right)
        # image.save("images/cut_first_name.jpg")
        return pytesseract.image_to_string(image, lang='eng')

    def surname(self, image):
        upper_left = Point(0.578 * image.size[1], 0.154 * image.size[0])
        lower_right = Point(0.603 * image.size[1], 0.263 * image.size[0])
        image = PassPage.prepare_image_part(image, upper_left, lower_right)
        # image.save("images/cut_surname.jpg")
        return pytesseract.image_to_string(image, lang='eng')

    def patronymic(self, image):
        upper_left = Point(0.679 * image.size[1], 0.209 * image.size[0])
        lower_right = Point(0.704 * image.size[1], 0.376 * image.size[0])
        image = PassPage.prepare_image_part(image, upper_left, lower_right)
        # image.save("images/cut_patronymic.jpg")
        return pytesseract.image_to_string(image, lang='eng')

    def birth_date(self, image):
        upper_left = Point(0.728 * image.size[1], 0)
        lower_right = Point(0.754 * image.size[1], 0.34 * image.size[0])
        image = PassPage.prepare_image_part(image, upper_left, lower_right)
        # image.save("images/cut_birth_date.jpg")
        return pytesseract.image_to_string(image, lang='rus')

    def birth_place(self, image):
        upper_left = Point(0.765 * image.size[1], 0.473 * image.size[0])
        lower_right = Point(0.81 * image.size[1], 0.91 * image.size[0])
        image = PassPage.prepare_image_part(image, upper_left, lower_right)
        # image.save("images/cut_birth_place.jpg")
        return pytesseract.image_to_string(image, lang='rus')

    def personal_number(self, image):
        upper_left = Point(0.729 * image.size[1], 0.622 * image.size[0])
        lower_right = Point(0.754 * image.size[1], 0.957 * image.size[0])
        image = PassPage.prepare_image_part(image, upper_left, lower_right)
        # image.save("images/cut_personal_number.jpg")
        return pytesseract.image_to_string(image, lang='eng')

    def issuing_date(self, image):
        upper_left = Point(0.886 * image.size[1], 0.065 * image.size[0])
        lower_right = Point(0.908 * image.size[1], 0.295 * image.size[0])
        image = PassPage.prepare_image_part(image, upper_left, lower_right)
        # image.save("images/cut_issuing_date.jpg")
        return pytesseract.image_to_string(image, lang='rus')

    def expiration_date(self, image):
        upper_left = Point(0.886 * image.size[1], 0.604 * image.size[0])
        lower_right = Point(0.908 * image.size[1], 0.95 * image.size[0])
        image = PassPage.prepare_image_part(image, upper_left, lower_right)
        # image.save("images/cut_expiration_date.jpg")
        return pytesseract.image_to_string(image, lang='rus')

    def create_file(self):
        path_to_file = "Result/" + self.pass_info["first_name"] + '_' + self.pass_info["surname"] + '_' +self.pass_info["patronymic"] + ".docx"
        path_to_template = "Docs/Belarus_pass.docx"
        super().create_file(path_to_file, path_to_template)
