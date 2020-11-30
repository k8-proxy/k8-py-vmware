from pprint import pprint
from unittest import TestCase

import pyVmomi

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
