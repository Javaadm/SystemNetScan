from Abstract_Documents.AbstractPage import AbstractPage
from pdf2image import convert_from_path


class AbstractDocument:
    def __init__(self, path_to_pdf, path_for_pages, fields, deletion_key=True, analysis_key=True, is_debugging=False):
        self.path_to_pdf = path_to_pdf
        self.path_for_pages = path_for_pages
        self.fields = fields
        self.deletion_key = deletion_key
        self.analysis_key = analysis_key
        self.is_debugging = is_debugging
        self.pages = self.get_numerated_pages()
        self.answer = self.get_text()

    def get_numerated_pages(self):
        return self.pdf_to_pages()

    def pdf_to_pages(self):
        self.debugging_log("pdf_to_pages", self.is_debugging)
        # return [PassPage(path_for_images + "out0.jpg", self.deletion_key, self.analysis_key)]
        pages = convert_from_path(self.path_to_pdf, 500)
        if self.analysis_key:
            for n in range(len(pages)):
                pages[n].save(self.path_for_images + 'out' + str(n) + '.jpg', 'JPEG')
        return [AbstractPage(self.path_for_images + 'out' + str(x) + '.jpg', self.deletion_key, self.analysis_key) for x in range(len(pages))]

    def get_text(self):
        for field in self.fields:
            self.pages[field["page_number"]].add_field(field)
        ans = []
        for page in self.pages:
            ans.append(page.get_text_from_page())
        return ans


