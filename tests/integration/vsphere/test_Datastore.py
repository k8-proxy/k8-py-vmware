from pprint import pprint
from unittest import TestCase

import pyVmomi
from osbot_utils.utils.Files import temp_file, file_contents
from osbot_utils.utils.Misc import random_string

from k8_vmware.Config import Config
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
        parent_folder = "an-parent-folder"
        folder_name   = f"{parent_folder}/random_name_new_folder_{random_string()}"

        assert self.datastore.folder_create(folder_name  ) == True        # create folder
        assert self.datastore.folder_delete(folder_name  ) == True        # delete folder
        assert self.datastore.folder_delete(folder_name  ) == False       # confirm it is not there
        assert self.datastore.folder_delete(parent_folder) == True        # although documentation says that delete is recursive, the parent folder was still here (https://vdc-download.vmware.com/vmwb-repository/dcr-public/b50dcbbf-051d-4204-a3e7-e1b618c1e384/538cf2ec-b34f-4bae-a332-3820ef9e7773/vim.FileManager.html#deleteFile)
        assert self.datastore.folder_delete(parent_folder) == False       # confirm parent folder was deleted

    ## misc tests

    # def test_delete_temp_folders_from_datastore(self):
    #     temp_folder_pattters = ["random_name_*", "test____enter__*", "unit_tests__*",
    #                             "tests__unit*", "unittest-test*"]
    #     print()
    #     for temp_folder_pattern in temp_folder_pattters:
    #         temp_folders = self.datastore.folders_names(temp_folder_pattern)
    #         for temp_folder in temp_folders:
    #             assert self.datastore.folder_delete(temp_folder) == True
    #             print(f"Deleted temp folder: {temp_folder}")