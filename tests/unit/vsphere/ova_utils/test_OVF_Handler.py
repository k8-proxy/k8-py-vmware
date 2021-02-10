import tarfile

import pyVmomi
from osbot_utils.utils.Files import file_exists

from k8_vmware.helpers.TestCase_OVA import TestCase_OVA
from k8_vmware.vsphere.ova_utils.File_Handle import FileHandle
from k8_vmware.vsphere.ova_utils.OVA import OVA
from k8_vmware.vsphere.ova_utils.OVF_Handler import Ovf_Hanlder
from k8_vmware.vsphere.ova_utils.Web_Handle import Web_Handle

class test_OvfHandler(TestCase_OVA):
    def setUp(self) -> None:
        self.ova          =   OVA()
        self.ova_handler  =   Ovf_Hanlder(self.ova_path)
        self.ova.download_ova_file(self.url, self.ova_path)


    def test_init(self):
        assert file_exists(self.ova_path)
        assert type(self.ova_handler.handle) is type(FileHandle(self.ova_path))

    def test_create_file_handle_for_url(self):
        response=self.ova_handler._create_file_handle(self.url)
        assert type(response) is type(Web_Handle(self.url))

    def test_create_file_handle_for_path(self):
        response=self.ova_handler._create_file_handle(self.ova_path)
        assert type(response) is type( FileHandle(self.ova_path) )

    def test_get_descriptor(self):
        response=self.ova_handler.get_descriptor()
        assert response is self.ova_handler.descriptor

    def test_upload_disks_failure_case(self):
        with self.assertRaises(Exception) as context:
            self.ova_handler.upload_disks(lease='lease',host='host')

    def test_get_device_url_failure_case(self):
        with self.assertRaises(Exception) as context:
            self.ova_handler.get_device_url(fileItem='fileItem',lease='lease')