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

    def source_dubl(self):
        for dir in self.patch_all:
            if '-' in dir:
                return dir








a = Sort()
b = a.source_dubl()
