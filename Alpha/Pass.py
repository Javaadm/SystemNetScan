from Alpha.PassPage import PassPage
from Alpha.PointVector import Point
from pdf2image import convert_from_path
import pytesseract


class Pass(object):
    def __init__(self, path_to_pdf: str, path_to_images: str):
        self.pages = self.pdf_to_pages(path_to_pdf, path_to_images)
        self.arrange_pages()
        self.fill_form()
        self.prepare_json()

    def pdf_to_pages(self, path_to_pdf, path_for_images):
        pages = convert_from_path(path_to_pdf, 500)
        #for n in range(len(pages)): #ACHTUNG IT'S ONLY FOR DEBUGGING
        #    pages[n].save(path_for_images + 'out' + str(n) + '.jpg', 'JPEG')
        return [PassPage(path_for_images + 'out' + str(x) + '.jpg') for x in range(len(pages))]

    def find_page(self, page_number):
        for page in self.pages:
            if self.validate_page(page, page_number):
                return page
            if self.validate_page(page.upside_down(), page_number):
                return page
        raise Exception("Page number " + str(page_number) + " is invalid!")

    def validate_page(self, page: PassPage, number):
        image = self.cut_page_number(page)
        #if(page.path == "images / out15.jpg") or (page.path == "images / out16.jpg"):
        text = pytesseract.image_to_string(image, lang='eng')
        print(page.path)
        print(text)
        print()
        return text.find(str(number)) != -1

    def arrange_pages(self):
        pass

    def validate_pass(self):
        pass

    def clear(self):
        pass

    def fill_form(self):
        pass

    def prepare_json(self):
        pass

