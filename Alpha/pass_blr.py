from PIL import Image, ImageDraw, ImageFont
from pdf2image import convert_from_path
import pytesseract
import tesserocr
from PIL import Image
import json
from Alpha.PassPage import PassPage
from Alpha.PointVector import Point
from Alpha.Pass import Pass


class BlrPass(Pass):
    def __init__(self, path_to_pdf, path_to_images):
        super().__init__(path_to_pdf=path_to_pdf, path_to_images=path_to_images)

    def arrange_pages(self):
        new_list = (self.find_pages([30, 32]))
        self.pages = [new_list[key] for key in sorted(new_list.keys())]

    def clear(self):
        pass

    def get_fields(self):
        fifteen_page = self.get_fifteen_page_text()
        # sixteen_page = self.get_sixteeen_page_text()
        pass_info = fifteen_page
        return pass_info

    def prepare_json(self):
        pass

    def cut_page_number(self, page, ang):
        crop = [x for x in page.get_image().size] * 2
        crop[0] = 0
        crop[1] = crop[1] * 0.029
        crop[2] = 0.167 * page.get_image().size[0]
        crop[3] = crop[1] + crop[2]
        image = page.get_image_part(Point(crop[1], crop[0]), Point(crop[3], crop[2]),
                                    brightness_border=150).rotate(90)
        # image.save(page.path[:-4] + "number" + ang + ".jpg")
        return image

    def get_fifteen_page_text(self):
        fifteen_page_text = dict()
        fifteen_page_image = self.pages[0].get_image()
        fifteen_page_text["name"] = self.name(fifteen_page_image)
        fifteen_page_text["surname"] = self.surname(fifteen_page_image)
        fifteen_page_text["patronymic"] = self.patronymic(fifteen_page_image)
        fifteen_page_text["birth_date"] = self.birth_date(fifteen_page_image)
        fifteen_page_text["birth_place"] = self.birth_place(fifteen_page_image)
        fifteen_page_text["personal_number"] = self.personal_number(fifteen_page_image)
        fifteen_page_text["issuing_date"] = self.issuing_date(fifteen_page_image)
        fifteen_page_text["expiration_date"] = self.expiration_date(fifteen_page_image)
        return fifteen_page_text

    def get_sixteen_page_text(self):
        pass

    def name(self, image):
        upper_left = Point(0.621 * image.size[1], 0.199 * image.size[0])
        lower_right = Point(0.654 * image.size[1], 0.324 * image.size[0])
        image = PassPage.prepare_image_part(image, upper_left, lower_right)
        # image.save("images/cut_name.jpg")
        return pytesseract.image_to_string(image, lang='rus')

    def surname(self, image):
        upper_left = Point(0.578 * image.size[1], 0.154 * image.size[0])
        lower_right = Point(0.603 * image.size[1], 0.263 * image.size[0])
        image = PassPage.prepare_image_part(image, upper_left, lower_right)
        # image.save("images/cut_surname.jpg")
        return pytesseract.image_to_string(image, lang='rus')

    def patronymic(self, image):
        upper_left = Point(0.679 * image.size[1], 0.209 * image.size[0])
        lower_right = Point(0.704 * image.size[1], 0.376 * image.size[0])
        image = PassPage.prepare_image_part(image, upper_left, lower_right)
        # image.save("images/cut_patronymic.jpg")
        return pytesseract.image_to_string(image, lang='rus')

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

    def get_json_passport(open_fname, main_path=""):
        birth_date_value = birth_date(open_fname, main_path)
        birth_place_value = birth_place(open_fname, main_path)
        personal_number_value = personal_number(open_fname, main_path)
        issuing_date_value = issuing_date(open_fname, main_path)
        expiration_date_value = expiration_date(open_fname, main_path)

        ret = {"birth date": birth_date_value, "birth_place": birth_place_value,
               "personal_number": personal_number_value,
               "issuing_date": issuing_date_value, "expiration_date": expiration_date_value}
        return ret
