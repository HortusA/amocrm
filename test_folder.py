from dubl import *
import os


def test_eins():
    assert os.path.isdir(path_root) == True


def test_zwei():
    assert os.listdir(path_root) != ''


def test_dray():
    assert os.access(path_root, os.W_OK)


def test_rec():
    list_all_folder = os.listdir(path_root)
    for checked_directory in list_all_folder:
        assert os.access(f'{path_root}{checked_directory}', os.W_OK) == True

