from unittest import TestCase

from osbot_utils.utils.Files import file_contents, temp_file, file_exists, file_delete
from osbot_utils.utils.Misc import random_string

from k8_vmware.vsphere.Datastore import Datastore
from k8_vmware.vsphere.Datastore_File import Datastore_File


class test_Datastore_File(TestCase):

    def setUp(self) -> None:
        self.ds_folder      = ''
        self.ds_file        = f"test_Datastore_File-{random_string()}.txt"
        self.datastore_file = Datastore_File(ds_folder=self.ds_folder, ds_file=self.ds_file)
        print()

    def test__init__(self):
        print('------')
        assert self.datastore_file.datastore.name == 'datastore1'
        assert self.datastore_file.ds_folder      == self.ds_folder
        assert self.datastore_file.ds_file        == self.ds_file

        #test other __init__ modes

        datastore_file = Datastore_File()
        assert datastore_file.datastore.name == 'datastore1'
        assert datastore_file.ds_folder      == ''
        assert datastore_file.ds_file        == ''

    def test_set_file_from_path_datastore(self):

        def confirm_values_are_set_correctly(ds_name, ds_folder, ds_file):                          # help method
            path_datastore = self.datastore_file.create_path_datastore(ds_name, ds_folder, ds_file)
            self.datastore_file.set_file_from_path_datastore(path_datastore)
            assert self.datastore_file.datastore.name == ds_name
            assert self.datastore_file.ds_folder      == ds_folder
            assert self.datastore_file.ds_file        == ds_file

        confirm_values_are_set_correctly("another datastore", "an folder/an subfolder", "an file")
        confirm_values_are_set_correctly("another datastore", ""                      , "an file")  # when ds_folder is not set
        confirm_values_are_set_correctly("another datastore", ""                      , ""       )  # when ds_file is not set
        confirm_values_are_set_correctly(""                 , ""                      , ""       )  # when ds_name is not set

    def test_upload__download(self):
        local_file = temp_file(contents="This is a local file - " + random_string())   # create local temp file

        self.datastore_file.upload(local_file)                                              # upload file to server
        tmp_file = self.datastore_file.download()                                           # download file from server

        assert file_exists(tmp_file)                                                        # confirm it exists
        assert file_contents(local_file) == file_contents(tmp_file)                         # confirm content matches the randomly generated temp content

        assert self.datastore_file.delete() is True                                         # delete temp file from data_store
        file_delete(local_file)                                                             # delete local temp file