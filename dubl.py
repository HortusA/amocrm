from pathlib import Path
import os
from config import *


class Sort:
    def __init__(self):
        self.path_root = path_root
        self.path_end = path_end
        self.path_beckap = path_beckap

    def source(self):
        self.patch_all = os.listdir(self.path_root)
        return self.patch_all

    def source_not_def(self):
        list_not_def = []
        for file_not_def in self.source():
            if not'-' in file_not_def:
                list_not_def.append(file_not_def)
        return list_not_def

    def source_def(self):
        list_dif = []
        for s in self.source():
            if '-' in s:
                list_dif.append(s)
        return list_dif

    def source_dubl(self):
        data_dubl=[]
        for n in self.source_def():
            split_data=(n.split('-'))
            if split_data[0] in self.source_not_def():
               data_dubl.append(split_data[0])
        return data_dubl


a = Sort()
print(a.source_not_def())
print(a.source_def())
print(a.source_dubl())
