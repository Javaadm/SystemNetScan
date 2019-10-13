from Alpha.PassPage import PassPage
from Alpha.PointVector import Point
from pdf2image import convert_from_path
import pytesseract


class Pass(object):
    def __init__(self, path_to_pdf: str, path_to_images: str):
        self.pages = self.pdf_to_pages(path_to_pdf, path_to_images)
        self.arrange_pages()
        self.pass_info = self.get_fields()
        self.prepare_json()

    def pdf_to_pages(self, path_to_pdf, path_for_images):
        pages = convert_from_path(path_to_pdf, 500)
        for n in range(len(pages)): #ACHTUNG IT'S ONLY FOR DEBUGGING
            pages[n].save(path_for_images + 'out' + str(n) + '.jpg', 'JPEG')
        return [PassPage(path_for_images + 'out' + str(x) + '.jpg') for x in range(len(pages))]

    def find_pages(self, pages_numbers):
        ret_pages = dict()
        for page in self.pages:
            image = self.cut_page_number(page, "1")
            text = pytesseract.image_to_string(image, lang='eng')
            # print(page.path)
            # print(text)
            # print()
            is_distinguished = False
            for number in pages_numbers:
                if text.find(str(number)) != -1:
                    ret_pages[number] = page
                    is_distinguished = True
                    break
            if(is_distinguished):
                continue
            image = self.cut_page_number(page.upside_down(), "2")
            text = pytesseract.image_to_string(image, lang='eng')
            print(page.path)
            print(text)
            print()
            for number in pages_numbers:
                if text.find(str(number)) != -1:
                    ret_pages[number] = page
                    break
        if(len(ret_pages) != len(pages_numbers)):
            raise Exception("Some pages indistinct!")
        return ret_pages

    def arrange_pages(self):
        pass

    def clear(self):
        pass

    def get_fields(self):
        pass

    def prepare_json(self):
        pass

