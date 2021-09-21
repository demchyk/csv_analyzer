import os
import zipfile


class Folder:
    def __init__(self, files_path, result_path):
        self.__files_path = files_path
        self.__result_path = result_path
        self.__class__.__processing_folder(self.__files_path, self.__result_path)

    @property
    def result_path(self):
        return self.__result_path

    @staticmethod
    def __unpack_unzip(files_path, result_path):
        os.chdir(files_path)
        for item in os.listdir(files_path):
            if item.endswith(".zip"):
                file_name = os.path.abspath(item)
                zip_ref = zipfile.ZipFile(file_name)
                zip_ref.extractall(result_path)
                zip_ref.close()
                os.remove(file_name)
        os.remove('.DS_Store')
        os.rmdir(files_path)

    @staticmethod
    def __remove_r(text):
        if text[-3:-1] == '_R':
            return(text[:-3])
        else:
            return(text)

    @classmethod
    def __duplicate_filtering(cls, size_files_list):
        detach_r_list = [[i, cls.__remove_r(size_files_list[i][0]), size_files_list[i][1]] for i in range(len(size_files_list))]
        detach_r_list.sort(key=lambda x: (x[1], x[2]), reverse=True)
        names_list = []
        result_list = []
        for item in detach_r_list:
            if item[1] not in names_list:
                names_list.append(item[1])
                result_list.append(size_files_list[item[0]][0])
        return(result_list)

    @classmethod
    def __processing_folder(cls, files_path, result_path):
        os.chdir(files_path)
        filtered_files_list = cls.__duplicate_filtering([[i.replace('.zip', ''), os.path.getsize(i)] for i in os.listdir(files_path)])
        for item in os.listdir(files_path):
            if str(item).replace('.zip', '') not in filtered_files_list:
                os.remove(item)
        cls.__unpack_unzip(files_path, result_path)
