import os.path
import json


class JsonWorker:

    # Сначала в инит передаешь ключи и путь к файлу (+ укажи, что создаешь новую ветку, если ключей еще нет new_path = True)
    # Теперь в нужной директории вызываешь get_current_directory() получаешь словарь всех уже сохраненных полей для данных ключей
    # Руками добавляешь в него свои значения, если требуется и запихиваешь обратно функцией replace_current_directory(твой массив)
    # В конце работы обязательно вызови save_json()
    # аргументы args - ключи, для доступа к полям(в порядке язык, тип, версия)
    # path_to_json - путь к базе данных
    # create_new - флаг, указывающий, нужно ли добавлять новый путь по заданным
    # ключам(защита от замусоривания базы данныx)
    def __init__(self, root_args, path_to_json="./Database/database.json", new_path=False):
        self.path_to_json = path_to_json
        self.root_args = root_args
        self.args = []
        if not(os.path.exists(path_to_json)):
            self.create_json(path_to_json)
        file = open(path_to_json, "r+")
        self.data = json.load(file)
        if new_path:
            self.make_path_root(root_args)
            file = open(path_to_json, "r+")
            self.data = json.load(file)
        self.working_root = self.get_working_root(self.root_args)
        self.working_directory = self.get_working_directory(self.args)

    def get_current_directory(self):
        return self.working_directory

    def replace_current_directory(self, new_directory):
        self.working_directory = new_directory
        self.apply_changes()

    # check if directory with args exists(checks path from the root)
    def is_exist_root(self, root_args):
        cursor = self.data
        for choice in root_args:
            if not(choice in cursor):
                return False
            cursor = cursor[choice]
        return True

    def is_exist(self, args):
        cursor = self.working_root
        for choice in args:
            if not(choice in cursor):
                return False
            cursor = cursor[choice]
        return True

    def get_working_root(self, root_args):
        if not self.is_exist_root(root_args):
            raise (Exception, "Key sequence doesnt' exist in database" + root_args)
        working_root = self.data
        for choice in root_args:
            working_root = working_root[choice]
        return working_root

    # gives directory by args from the root
    def get_working_directory(self, args):
        if not self.is_exist(args):
            raise (Exception, "Key sequence doesnt' exist in database" + self.root_args + args)
        working_directory = self.working_root
        for choice in args:
            working_directory = working_directory[choice]
        return working_directory

    # Nothing debugged. Be especially cautious when using this function.
    def save_json(self, path_to_json=None):
        if path_to_json is None:
            path_to_json = self.path_to_json
        # print(self.root_args)
        self.apply_changes()
        new_data = self.get_working_root(self.root_args)
        for i in range(1, len(self.root_args)+1):
            prev_data = new_data
            new_data = self.get_working_root(self.root_args[:-i])
            new_data[self.root_args[-i]] = prev_data
        # whole = JsonWorker([], self.path_to_json)
        # whole.move_to(self.root_args[:-1])
        # print(self.root_args)
        # whole.add_field(self.root_args[-1], self.working_root, rewrite=True)
        # whole.apply_changes()
        with open(path_to_json, "w+") as output:
            json.dump(new_data, output)
        self.__init__(self.root_args, self.path_to_json)

    # The most crutched function for making path to root if it hasn't been created yet
    def make_path_root(self, root_args):
        working_root = self.data
        path_maker = JsonWorker([], self.path_to_json)
        for arg in root_args:
            if not(arg in path_maker.working_directory.keys()):
                path_maker.add_field(arg)
            path_maker.step_into(arg)
        path_maker.save_json()

    def apply_changes(self):
        working_directory = self.working_directory
        args = self.args
        for i in range(1, len(args) + 1):
            new_args = args[:-i]
            dir_with_changes = working_directory
            working_directory = (self.get_working_directory(new_args))
            working_directory[args[-i]] = dir_with_changes
        self.working_root = working_directory
        self.working_directory = self.get_working_directory(self.args)

    # I dont' aware this method is needed. I will delete it if there will be no need for it
    def discard_changes(self):
        pass

    # moves one step back in tree
    def step_back(self):
        self.apply_changes()
        self.args = self.args[:-1]
        print(self.args)
        self.working_directory = self.get_working_directory(self.args)

    # (important to save all changes in tree even if you leave node without saving!)
    def step_into(self, next_key):
        self.apply_changes()
        if not(next_key in self.working_directory):
            raise(Exception, "No such key in current working directory" + next_key)
        self.args.append(next_key)
        self.working_directory = self.working_directory[next_key]

    def move_to(self, args):
        self.apply_changes()
        self.args = args
        self.working_directory = self.get_working_directory(self.args + args)

    # adds a field to a current working directory
    def add_field(self, field_name, value=None, rewrite=False):
        if value is None:
            field = dict()
        else:
            field = value
        if (field_name in self.working_directory) and not rewrite:
            raise(Exception, "directory protected from rewriting: " + field_name)
        self.working_directory[field_name] = field
        self.apply_changes()

    # deletes current directory and moves cursor one level back
    def delete_node(self):
        args = self.args
        self.step_back()
        self.working_directory.pop([args[-1]])

    def print_data(self):
        pass

    def create_train_data_field(self, doc_number, fields, stamps, pages):
        field = dict()
        if doc_number in self.working_directory:
            raise(Exception, "trying to rewrite existing document with number:"
                  + doc_number)
        field["fields"] = fields
        field["stamps"] = stamps
        field["pages"] = pages
        self.add_field(doc_number, field)
        self.apply_changes()

    def create_work_data_fields(self,fields_name, fields):
        self.add_field(fields_name, fields)
        self.apply_changes()



    # def add_work_data_field(self, field_name, coords, page_number, lang,
    #                    is_hand_writing, is_having_digit, params, pattern):
    #     field = dict()
    #     field["coords"] = coords
    #     field["page_number"] = page_number
    #     field["lang"] = lang
    #     field["is_hand_writing"] = is_hand_writing
    #     field["is_having_digit"] = is_having_digit
    #     field["params"] = params
    #     self.add_field(field_name=field_name, value=field)
    #     self.apply_changes()



    # Bellow are located only static methods
    @staticmethod
    def create_json(path_to_json):
        with open(path_to_json, "w+") as f:
            json.dump(dict(), f)

