import os
import zipfile


class Net_Folder:
    def __new__(cls, path):
        if cls.__check_requirements(path) and cls.__check_input_data(path):
            return super().__new__(cls)
        else:
            return None

    def __init__(self, path):
        self.__path = path
        self.__class__.__processing_input(self.__path)

    @property
    def path(self):
        return self.__path

    @staticmethod
    def __check_requirements(path):
        formula = path + "/requirements/formula.txt"
        keys = path + "/requirements/keys.txt"
        if os.path.isfile(formula) and os.path.isfile(keys):
            return True
        else:
            return False

    @staticmethod
    def __check_input_data(path):
        cur_path = path + "/input_data/"
        if os.listdir(cur_path):
            return True
        else:
            return False

    @staticmethod
    def __processing_input(path):
        cur_path = path + "/input_data"
        for address, dirs, files in os.walk(cur_path):
            for file in files:
                if file.endswith(".zip"):
                    zip_ref = zipfile.ZipFile(os.path.join(address, file))
                    zip_ref.extractall(path + "/processed_files/")
                    zip_ref.close()



lte = Net_Folder(os.path.dirname(os.path.realpath('__file__')) + "/ZTE/LTE")
