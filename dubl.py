import os
import shutil

path_root = '/home/hortus/Документы/leads/'


class Sort:
    def __init__(self):
        self.path_root = path_root
        self.list_all_folder = ''

    @property
    def search(self):
        self.list_all_folder = os.listdir(self.path_root)
        list_of_duplicate = []
        for checked_directory in self.list_all_folder:
            if '-' in checked_directory:
                split_directory = (checked_directory.split('-'))
                if split_directory[0] in self.list_all_folder:
                    get_files = os.listdir(f'{path_root}/{split_directory[0]}')
                    for one_directory_file in get_files:
                        if not os.path.exists(f'{path_root}/{checked_directory}/{one_directory_file}'):
                            print('Файла {g} будет скопирован')
                            shutil.copy(f'{path_root}/{split_directory[0]}/{one_directory_file}',
                                        f'{path_root}/{checked_directory}/{one_directory_file}')
                        else:
                            print(f'Файл с именем {one_directory_file} в директории {checked_directory} уже существует')

                    list_of_duplicate.append(checked_directory)
        return list_of_duplicate


a = Sort()
print(a.search)
