import os.path
import json


class JsonWorker:

    # аргументы args - ключи, для доступа к полям(в порядке язык, тип, версия) (в будущем планирую добавить возможность
    # перемещения по дереву json'а)
    # path_to_json - путь к базе данных
    # create_new - флаг, указывающий, нужно ли добавлять новый(или переписывать старый) документ по заданным
    # ключам(защита от замусоривания базы данныx)
    def __init__(self, root_args, path_to_json="./Database/database.json", create_new=False):
        self.path_to_json = path_to_json
        self.root_args = root_args
        self.args = []
        if not(os.path.exists(path_to_json)):
            self.create_json(path_to_json)
        file = open(path_to_json, "r+")
        self.data = json.load(file)
        if create_new:
            self.make_path(root_args)
        self.working_root = self.get_working_root(root_args)
        self.working_directory = self.get_working_directory(self.args)

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
            raise (Exception, "Key sequence doesnt' exist in databse")
        working_root = self.data
        for choice in root_args:
            working_root = working_root[choice]
        return working_root

    # gives directory by args from the root
    def get_working_directory(self, args):
        if not self.is_exist(args):
            raise (Exception, "Key sequence doesnt' exist in databse")
        working_directory = self.working_root
        for choice in args:
            working_directory = working_directory[choice]
        return working_directory

    # Nothing debugged. Be especialy cautious using this function.
    def save_json(self, path_to_json=None):
        if path_to_json is None:
            path_to_json = self.path_to_json
        self.apply_changes()
        whole = JsonWorker([], self.path_to_json)
        whole.move_to(self.root_args)
        whole.add_field(self.working_root)
        whole.apply_changes()
        with open(path_to_json, "w+") as output:
            json.dump(whole.working_root, output)
        self.__init__(self.root_args, self.path_to_json)

    # The most crutched function for making path to root if it hasn't been created yet
    def make_path(self, root_args):
        working_root = self.data
        path_maker = JsonWorker(self.root_args, self.path_to_json)
        for i in range(root_args):
            new_args = root_args[:1 + i -len(root_args)]
            if not(path_maker.is_exist(new_args)):
                path_maker.add_field(root_args[i])
            path_maker.step_into(root_args[i])
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
        self.working_directory = self.get_working_directory(self.args)

    # (important to save all changes in tree even if you leave node without saving!)
    def step_into(self, next_key):
        self.apply_changes()
        if not(next_key in self.working_directory):
            raise(Exception, "No such key in current working directory")
        self.working_directory = self.working_directory[next_key]

    def move_to(self, args):
        self.apply_changes()
        self.working_directory = self.get_working_directory(self.args + args)

    # adds a field to a current working directory
    def add_field(self, field_name, value=None):
        if value is None:
            field = dict()
        else:
            field = value
        self.working_directory[field_name] = field
        self.apply_changes()

    # deletes current directory and moves cursor one level back
    def delete_node(self):
        args = self.args
        self.step_back()
        self.working_directory.pop([args[-1]])

    def print_data(self):
        pass

    # Bellow are located only static methods
    @staticmethod
    def create_json(path_to_json):
        with open(path_to_json, "w+") as f:
            json.dump(dict(), f)

