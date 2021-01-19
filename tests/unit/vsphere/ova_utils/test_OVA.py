from osbot_utils.utils.Files import file_exists

from k8_vmware.helpers.TestCase_OVA import TestCase_OVA
from k8_vmware.vsphere.ova_utils.OVA import OVA

class test_OVA(TestCase_OVA):
    def setUp(self) -> None:
        self.ova = OVA()

    def test__init__(self):
        assert self.ova.sdk is not None

    def test_download_ova_file(self):
        self.ova.download_ova_file(self.url,self.ova_path)
        assert file_exists(self.ova_path)

    def test_upload_ova_file(self):
        self.ova.download_ova_file(self.url, self.ova_path)
        assert file_exists(self.ova_path)
        response=self.ova.upload_ova(self.ova_path)
        assert response is 0
        self.vm = self.ova.sdk.find_by_name(self.vm_name)
        assert self.vm is not None
        self.vm.task().delete()

    # def test_upload_ova_web(self):
    #     url = "https://packages.vmware.com/photon/4.0/Beta/ova/photon-hw11-4.0-d98e681.ova"
    #     self.ova.upload_ova(url)
    #     self.vm = self.ova.sdk.find_by_name("Photon OS")
    #     assert self.vm is not None
    #     self.vm.task().delete()