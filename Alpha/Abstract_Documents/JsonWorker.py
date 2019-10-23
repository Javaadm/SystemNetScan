import os.path
import json


class JsonWorker:

    # аргументы args - ключи, для доступа к полям(в порядке язык, тип, версия) (в будущем планирую добавить возможность
    # перемещения по дереву json'а)
    # path_to_json - путь к базе данных
    # create_new - флаг, указывающий, нужно ли создавать новый документ по заданным
    # ключам(защита от замусоривания базы данныx)
    def __init__(self, args, path_to_json="./Database/database.json", create_new=False):
        self.path_to_json = path_to_json
        self.args = args
        if not(os.path.exists(path_to_json)):
            self.create_json(path_to_json)
        file = open(path_to_json, "r+")
        self.data = json.load(file)
        if not(create_new):
            self.working_directory = self.get_working_directory(args)

    def is_exist(self, args):
        cursor = self.data
        for choice in args:
            if not(choice in cursor):
                return False
            cursor = cursor[choice]
        return True

    def get_working_directory(self, args):
        if not self.is_exist(args):
            raise (Exception, "Key sequence doesnt' exist in databse")
        working_directory = self.data
        for choice in args:
            working_directory = working_directory[choice]
        return working_directory

    # Nothing debugged. Be especialy cautious using this function.
    def save_json(self, path_to_json=None):
        if path_to_json is None:
            path_to_json = self.path_to_json
        working_directory = self.working_directory
        args = self.args
        for i in range(1, len(args) + 1):
            new_args = args[:-i]
            working_directory = self.get_working_directory(new_args)[args[-i]] = working_directory
        with open(path_to_json, "w+") as output:
            json.dump(working_directory, output)

    # moves one step back in tree
    def step_back(self):
        pass

    # (important to save all changes in tree even if you leave node without saving!)
    def step_to(self, next_key):
        pass

    def add_field(self):
        pass

    # I go sleep. I think it's enough to understand basics of json I wanna make.

    # Bellow are located only static methods
    @staticmethod
    def create_json(path_to_json):
        with open(path_to_json, "w+") as f:
            json.dump(dict(), f)

