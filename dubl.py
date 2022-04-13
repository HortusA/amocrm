from os import listdir, path
import shutil
import pathlib

path_to_leads = '/home/hortus/Документы/leads/'


class CheckingLeads:
    def __init__(self):
        self.path_to_leads = path_to_leads
        self.list_of_duplicate = []
        self.list_separated_leads = []
        self.list_files_in_folder = []

    @property
    def get_list_leads(self):
        if path.isdir(self.path_to_leads):
            return listdir(self.path_to_leads)
        else:
            print('путь к каталоку не являться верным')

    def get_separated_leads(self):
        for name_leads in self.get_list_leads:
            if path.isdir(pathlib.Path(path_to_leads, name_leads)):
                if '-' in name_leads:
                    self.list_separated_leads.append(name_leads.split('-'))
            else:
                print(f'Обратите внимание на файл{name_leads}')
                
        return self.list_separated_leads

    def transferring_leads_files(self):
        for one_leads in self.get_separated_leads():
            if one_leads[0] in self.get_list_leads:
                get_files = listdir(pathlib.Path(path_to_leads, one_leads[0]))
                for one_file_from_leads in get_files:
                    path_from_ware = (pathlib.Path(path_to_leads, one_leads[0], one_file_from_leads))
                    path_ware = (pathlib.Path(path_to_leads, '-'.join(one_leads), one_file_from_leads))
                    if not path.exists(path_ware):
                        print(f'Файла {one_file_from_leads} будет скопирован')
                        shutil.copy(path_from_ware, path_ware)
                    else:
                        print(f'Файл {one_file_from_leads} в директории {("-".join(one_leads))} уже существует')


a = CheckingLeads()
a.transferring_leads_files()
