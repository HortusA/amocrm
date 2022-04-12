from os import listdir, path
import shutil

path_to_leads = '/home/hortus/Документы/leads/'


class CheckingLeads:
    def __init__(self):
        self.path_to_leads = path_to_leads
        self.list_of_duplicate = []
        self.list_separated_leads = []
        self.list_files_in_folder = []

    @property
    def get_list_leads(self):
        return listdir(self.path_to_leads)

    def get_separated_leads(self):
        for name_leads in self.get_list_leads:
            if '-' in name_leads:
                self.list_separated_leads.append(name_leads.split('-'))
        return self.list_separated_leads

    def transferring_leads_files(self):
        for one_leads in self.get_separated_leads():
            if one_leads[0] in self.get_list_leads:
                get_files = listdir(f'{path_to_leads}/{one_leads[0]}')
                for one_file_from_leads in get_files:
                    path_from_ware = f'{path_to_leads}/{one_leads[0]}/{one_file_from_leads}'
                    path_ware = f'{path_to_leads}/{one_leads[0]}-{one_leads[1]}/{one_file_from_leads}'
                    if not path.exists(path_ware):
                        print(f'Файла {one_file_from_leads} будет скопирован')
                        shutil.copy(path_from_ware, path_ware)
                    else:
                        print(f'Файл {one_file_from_leads} в директории {one_leads[0]}-{one_leads[1]} уже существует')


a = CheckingLeads()
a.transferring_leads_files()
