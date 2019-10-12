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
        new_list = []
        new_list.append(self.find_page(30))
        new_list.append(self.find_page(32))
        self.pages=new_list

    def clear(self):
        pass

    def fill_form(self):
        pass

    def prepare_json(self):
        pass

    def cut_page_number(self, page):
        crop = [x for x in page.get_image().size] * 2
        crop[0] = 0
        crop[1] = 0.013 * page.get_image().size[1]
        crop[2] = 0.162 * page.get_image().size[0]
        crop[3] = crop[1] + crop[2]
        image = page.get_image_part(Point(crop[1], crop[0]), Point(crop[3], crop[2]),
                                        brightness_border=160)
        return image.rotate(90)

    def birth_date(self, image):
        pass
        image = image.convert('RGB')
        base_crop = image.size()
        upper_left = Point()
        lower_right = Point()
        return pytesseract.image_to_string(self.prepare_image_part(image, upper_left,
                                                                   lower_right), lang='rus')


    def birth_place(open_fname, main_path, brightness_border=180, scale=1):
        birth_place_path = main_path + "birth_place.jpg"
        base = Image.open(open_fname).convert('RGB')
        image_crop = [x // 2 for x in base.size] * 2;
        # print(image_crop)
        image_crop[0] += -30
        image_crop[1] += 860
        image_crop[2] += 1050
        image_crop[3] += 1060
        # print(image_crop)
        # show(base, image_crop)
        prepare(open_fname, birth_place_path, image_crop, brightness_border=brightness_border, scale=scale)
        return pytesseract.image_to_string(Image.open(birth_place_path), lang='rus')


    def personal_number(open_fname, main_path, brightness_border=180, scale=1):
        personal_number_path = main_path + "personal_number.jpg"
        base = Image.open(open_fname).convert('RGB')
        image_crop = [x // 2 for x in base.size] * 2;
        image_crop[0] += 370
        image_crop[1] += 760
        image_crop[2] += 1120
        image_crop[3] += 860
        prepare(open_fname, personal_number_path, image_crop, brightness_border=brightness_border, scale=scale)
        return pytesseract.image_to_string(Image.open(personal_number_path), lang='eng')


    def issuing_date(open_fname, main_path, brightness_border=180, scale=1):
        issuing_date_path = main_path + "issuing_date.jpg"
        base = Image.open(open_fname).convert('RGB')
        image_crop = [x // 2 for x in base.size] * 2;
        image_crop[0] += -1010
        image_crop[1] += 1330
        image_crop[2] += -470
        image_crop[3] += 1400
        prepare(open_fname, issuing_date_path, image_crop, brightness_border=brightness_border, scale=scale)
        return pytesseract.image_to_string(Image.open(issuing_date_path), lang='rus')


    def expiration_date(open_fname, main_path, brightness_border=180, scale=1):
        expiration_date_path = main_path + "expiration_date.jpg"
        base = Image.open(open_fname).convert('RGB')
        image_crop = [x // 2 for x in base.size] * 2;
        image_crop[0] += 350
        image_crop[1] += 1330
        image_crop[2] += 1150
        image_crop[3] += 1400
        prepare(open_fname, expiration_date_path, image_crop, brightness_border=brightness_border, scale=scale)
        return pytesseract.image_to_string(Image.open(expiration_date_path), lang='rus')


    def get_json_passport(open_fname, main_path=""):
        birth_date_value = birth_date(open_fname, main_path)
        birth_place_value = birth_place(open_fname, main_path)
        personal_number_value = personal_number(open_fname, main_path)
        issuing_date_value = issuing_date(open_fname, main_path)
        expiration_date_value = expiration_date(open_fname, main_path)

        ret = {"birth date": birth_date_value, "birth_place": birth_place_value, "personal_number": personal_number_value,
               "issuing_date": issuing_date_value, "expiration_date": expiration_date_value}
        return ret


