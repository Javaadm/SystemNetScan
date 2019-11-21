from Abstract_Documents.JsonWorker import JsonWorker

class AbstractPage:

    def __init__(self, name, coords, lang, params, is_hand_writing=False, is_having_digit=False):
        self.name = name
        self.coords = coords
        self.lang = lang
        self.is_hand_writing = is_hand_writing
        self.is_having_digit = is_having_digit
        self.params = params
        self.start_processing()


