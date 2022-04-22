from os import listdir, path
import shutil
import pathlib
from pathlib import Path
import os
import time

path_to_leads = '/home/hortus/Документы/leads/'


class CheckingLeads:
    def __init__(self):
        self.path_to_leads = path_to_leads
        self.list_of_duplicate = []
        self.list_separated_leads = []
        self.list_files_in_folder = []
        self.dict_report = {}

    def write_file(self, name_report):
        name_files = time.strftime("%Y%m%d-%H%M%S")
        with open(name_files, 'w') as File:

            for i in name_report:
                File.write(f'{i} ' + '\n')

    @property
    def get_list_leads(self):
        if path.isdir(self.path_to_leads):
            return listdir(self.path_to_leads)
        else:
            print('проверьте путь к каталогу')

    def copy_file(self, dir_def):
        get_files = listdir(pathlib.Path(path_to_leads, '-'.join(dir_def)))
        for file in get_files:
            path_from_ware = (pathlib.Path(path_to_leads, '-'.join(dir_def), file))
            path_ware = (pathlib.Path(path_to_leads, dir_def[0], file))
            if not path.exists(path_ware):
                if path.isfile(pathlib.Path(path_to_leads, path_from_ware)):
                    shutil.copy(path_from_ware, path_ware)
                else:
                    shutil.copytree(path_from_ware, path_ware)
                self.list_of_duplicate.append(
                                {
                                    "Исходная директория": path_from_ware,
                                    "Конечная директория": {
                                        "Путь": path_from_ware,
                                        "файл": file,
                                        "Тип оперции": "Копирование"
                                            }
                                }
                            )

            else:
                self.list_of_duplicate.append(
                                {
                                    "Исходная директория": path_from_ware,
                                    "Конечная директория": {
                                        "Путь": path_from_ware,
                                        "файл": file,
                                        "Тип оперции": "Ошибка. Файл в каталоге присутствует"
                                            }
                                }
                            )
        self.dict_report.update(self.list_of_duplicate)

    def transferring_leads_files(self):
        for dir_in_leads in self.get_list_leads:
            if path.isdir(pathlib.Path(path_to_leads, dir_in_leads)) and \
                    len(os.listdir(pathlib.Path(path_to_leads, dir_in_leads))) != 0:
                if '-' in dir_in_leads:
                    dir_def = (dir_in_leads.split('-'))
                    if dir_def[0] in self.get_list_leads:
                        self.copy_file(dir_def)
                    else:
                        if dir_def[0] not in self.get_list_leads:
                            os.makedirs(pathlib.Path(path_to_leads, dir_def[0]))
                            self.list_of_duplicate.append(
                                {
                                    "Исходная директория": path_to_leads,
                                    "Конечная директория": {
                                        "Путь": pathlib.Path(path_to_leads, dir_def[0]),
                                        "Директория": dir_def[0],
                                        "Тип оперции": "Директория отсутствовала и быда создана"
                                    }
                                }
                            )
                            self.copy_file(dir_def)


a = CheckingLeads()
a.transferring_leads_files()
a.write_file(a.list_of_duplicate)
