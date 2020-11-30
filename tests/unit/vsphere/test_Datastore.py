from pprint import pprint
from unittest import TestCase

import pyVmomi
from osbot_utils.utils.Misc import random_string

from k8_vmware.vsphere.Datastore import Datastore
from k8_vmware.vsphere.Task import Task


class test_Datastore(TestCase):

    def setUp(self):
        self.datastore = Datastore()

    def test__init__(self):
        assert self.datastore.name == 'datastore1'

    def test_datastore(self):
        datastore = self.datastore.datastore()
        assert datastore.info.name == self.datastore.name

    def test_info(self):
        info = self.datastore.info()
        assert type(info['Capacity']) is str
        assert info['Name']           == self.datastore.name
        assert type(info['SSD'])      is bool
        assert type(info['Type'])     is str
        assert type(info['UUID'])     is str

    def test_folders(self):
        folders = self.datastore.folders()
        assert len(folders) > 0
        assert set(folders[0]) == {'Owner', 'Modified', 'FolderName', 'Size'}

    def test_folders_names(self):
        folders = self.datastore.folders_names()
        assert len(folders) > 0

    def test_search_files(self):
        files = self.datastore.files()
        assert len(files) > 0

    def test_search_files_names(self):
        files = self.datastore.files_names()
        assert len(files) > 0

    def test_search_files_paths(self):
        files = self.datastore.files("*")
        assert len(files) > 0


    def test_folder_create__delete(self):

        folder_name = f"random_name_new_folder_{random_string()}"

        assert self.datastore.folder_create(folder_name) == True
        assert self.datastore.folder_delete(folder_name) == True



    ## misc tests

    def test_delete_temp_folders_from_datastore(self):
        temp_folder_pattters = ["random_name_*", "test____enter__*", "unit_tests__*",
                                "tests__unit*", "unittest-test*"]
        print()
        for temp_folder_pattern in temp_folder_pattters:
            temp_folders = self.datastore.folders_names(temp_folder_pattern)
            for temp_folder in temp_folders:
                assert self.datastore.folder_delete(temp_folder) == True
                print(f"Deleted temp folder: {temp_folder}")