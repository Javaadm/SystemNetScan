from Abstract_Documents.AbstractPage import AbstractPage
from Abstract_Documents.JsonWorker import JsonWorker
from pdf2image import convert_from_path


class AbstractDocument:
    # json_keys must be plain array with indexes from 0 to 2 or from 0 to 1!!!(document_type, lang, version)
    def __init__(self, path_to_pdf, path_for_pages, json_keys, path_to_json, deletion_key=True, analysis_key=True, is_debugging=False):
        self.path_to_pdf = path_to_pdf
        self.path_for_pages = path_for_pages
        self.path_to_json = path_to_json
        self.json_keys = json_keys
        if len(self.json_keys) == 2:
            self.json_keys.append(0)
        if self.json_keys[2] is None:
            self.json_keys[2] = 0
        self.json = JsonWorker(self.json_keys, path_to_json=self.path_to_json)
        self.json.step_into("fields")
        self.fields = self.json.get_current_directory()
        self.json.step_back()
        self.deletion_key = deletion_key
        self.analysis_key = analysis_key
        self.is_debugging = is_debugging
        self.debugging_log(self.fields)
        self.pages = self.get_numerated_pages()
        self.answer = self.get_text()

    def debugging_log(self, text):
        if self.is_debugging:
            print(text)

    def get_numerated_pages(self):
        return self.pdf_to_pages()

    def pdf_to_pages(self):
        self.debugging_log("pdf_to_pages")
        # return [PassPage(path_for_pages + "out0.jpg", self.deletion_key, self.analysis_key)]
        pages = convert_from_path(self.path_to_pdf, 500)
        if self.analysis_key:
            for n in range(len(pages)):
                pages[n].save(self.path_for_pages + 'out' + str(n) + '.jpg', 'JPEG')
        return [AbstractPage(self.path_for_pages + 'out' + str(x) + '.jpg', self.deletion_key, self.analysis_key) for x in range(len(pages))]

    def get_text(self):
        for field in self.fields:
            self.debugging_log(field)
            self.debugging_log(int(field["page_number"]))
            self.pages[int(field["page_number"])].add_field(field)
        ans = []
        for page in self.pages:
            ans.append(page.get_text_from_page())
        return ans


