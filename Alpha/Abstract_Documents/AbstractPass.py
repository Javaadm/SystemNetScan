from .AbstractDocument import AbstractDocument


class AbstractPass(AbstractDocument):

    def __init__(self, path_to_json):
        super().__init__(path_to_json=path_to_json)
