import os
import zipfile
import shutil

class Net_Folder:

    def __init__(self, path):
        self.__path = path
        self.__zipfiles_list = self.__class__.__get_ziplist_by_size(self.__get_input_files_path(self.__path))

    @property
    def csv_path(self):
        return self.__path + "/processed_files"

    @property
    def formula(self):
        return self.__path + "/requirements/formula.txt"

    @property
    def keys(self):
        return self.__path + "/requirements/keys.txt"

    @property
    def claster(self):
        return self.__path + "/requirements/cluster.txt"

    @property
    def zipfiles_list(self):
        return self.__zipfiles_list

    @staticmethod
    def __check_requirements(path):
        formula = path + "/requirements/formula.txt"
        keys = path + "/requirements/keys.txt"
        input_files_path = path + '/requirements/datapath.txt'
        cluster = path + '/requirements/cluster.txt'
        if os.path.isfile(formula) and os.path.isfile(keys) and os.path.isfile(input_files_path) and os.path.isfile(cluster):
            return True
        else:
            return False

    @staticmethod
    def __get_input_files_path(path):
        f = open(path + '/requirements/datapath.txt')
        return f.readline().strip()

    @classmethod
    def __processing_input(cls, path):
        for address, dirs, files in os.walk(path + "/input_data/"):
            for file in files:
                if file.endswith(".zip"):
                    zip_ref = zipfile.ZipFile(os.path.join(address, file))
                    zip_ref.extractall(path + "/processed_files/")
                    zip_ref.close()
        # cls.__remove_directory_content(path + "/input_data/")

    @classmethod
    def __get_ziplist_by_folder(cls, path):
        li = [f.path for f in os.scandir(
            path) if f.is_dir() and os.listdir(f)]
        rez = [[] for item in li]
        for i in range(len(li)):
            for address, dirs, files in os.walk(li[i]):
                for file in files:
                    if file.endswith(".zip"):
                        rez[i].append(os.path.join(address, file))
        return rez

    @classmethod
    def __get_ziplist_by_size(cls, path):
        temp_li = []
        for address, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".zip"):
                    temp_li.append([os.path.join(address, file), os.path.getsize(os.path.join(address, file))])
        temp_li.sort(key=lambda x: x[0])
        rez = [[]]
        i = 0
        size_counter = 0
        for item in temp_li:
            size_counter += item[1]
            if size_counter >= ((10**9)/2):
                rez.append([])
                i += 1
                rez[i].append(item[0])
                size_counter = 0
            else:
                rez[i].append(item[0])
        return rez

    @staticmethod
    def __remove_directory_content(dir):
        for files in os.listdir(dir):
            path = os.path.join(dir, files)
            try:
                shutil.rmtree(path)
            except OSError:
                os.remove(path)


# time1 = time.time()
# time2 = time.time()
# print(time2 - time1)
