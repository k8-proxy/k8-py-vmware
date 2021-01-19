from unittest.mock import Mock

from osbot_utils.utils.Files import file_exists

from k8_vmware.helpers.TestCase_OVA import TestCase_OVA
from k8_vmware.vsphere.ova_utils.OVA import OVA
from k8_vmware.vsphere.ova_utils.OVF_Handler import OvfHandler


class test_OvfHandler(TestCase_OVA):
    def setUp(self) -> None:
        self.ova = OVA()
        self.ova.download_ova_file(self.url, self.ova_path)
        self.ova_handler = OvfHandler(self.ova_path)

    def test_init(self):
        assert file_exists(self.ova_path)
        assert self.ova_handler is not None

    def test_create_file_handle(self):
        response=self.ova_handler._create_file_handle(self.url)
        assert response is not None
        assert response.tell() is not None
        assert response.seekable() is True

    def test_get_descriptor(self):
        response=self.ova_handler.get_descriptor()
        assert response is not None

    def test_upload_disks_failure_case(self):
        with self.assertRaises(Exception) as context:
            self.ova_handler.upload_disks(lease='lease',host='host')
        assert context is not None

    def test_get_device_url_failure_case(self):
        with self.assertRaises(Exception) as context:
            self.ova_handler.get_device_url(fileItem='fileItem',lease='lease')
        assert context is not None