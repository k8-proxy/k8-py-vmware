import tarfile

import pyVmomi
from osbot_utils.utils.Files import file_exists

from k8_vmware.helpers.TestCase_OVA import TestCase_OVA
from k8_vmware.vsphere.ova_utils.File_Handle import FileHandle
from k8_vmware.vsphere.ova_utils.OVA import OVA
from k8_vmware.vsphere.ova_utils.OVF_Handler import OvfHandler
from k8_vmware.vsphere.ova_utils.Web_Handle import WebHandle


class test_OvfHandler(TestCase_OVA):
    def setUp(self) -> None:
        self.ova = OVA()
        self.ova.download_ova_file(self.url, self.ova_path)
        self.ova_handler = OvfHandler(self.ova_path)

        self.host       =    self.ova.sdk.server_details().get('host')

        ovfManager      =    self.ova.sdk.content().ovfManager
        rp              =    self.ova.sdk.resource_pool()
        ds              =    self.ova.sdk.datastore()
        dc              =    self.ova.sdk.datacenter()
        cisp            =    pyVmomi.vim.OvfManager.CreateImportSpecParams()
        self.cisr       =    ovfManager.CreateImportSpec(self.ova_handler.get_descriptor(), rp, ds, cisp)
        self.lease = rp.ImportVApp(self.cisr.importSpec, dc.vmFolder)

    def test_set_spec(self):
        self.ova_handler.set_spec(self.cisr)
        assert self.ova_handler.spec is self.cisr

    def test_init(self):
        assert file_exists(self.ova_path)
        assert type(self.ova_handler.handle) is type(FileHandle(self.ova_path))

    def test_create_file_handle_for_url(self):
        response=self.ova_handler._create_file_handle(self.url)
        assert type(response) is type( WebHandle(self.url) )

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

    # def test_upload_disk(self):
    #     self.ova_handler.set_spec(self.cisr)
    #     result = self.ova_handler.upload_disks(self.lease , self.host)
    #     assert result is 0
