from unittest import TestCase
from urllib.request import urlopen
from osbot_utils.utils.Files import file_exists

from k8_vmware.helpers.TestCase_OVA import TestCase_OVA
from k8_vmware.vsphere.OVA import OVA, OvfHandler, FileHandle, WebHandle

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
        self.ova.upload_ova(self.ova_path)
        self.vm = self.ova.sdk.find_by_name(self.vm_name)
        assert self.vm is not None
        self.vm.task().delete()

    # def test_upload_ova_web(self):
    #     url = "https://packages.vmware.com/photon/4.0/Beta/ova/photon-hw11-4.0-d98e681.ova"
    #     self.ova.upload_ova(url)
    #     self.vm = self.ova.sdk.find_by_name("Photon OS")
    #     assert self.vm is not None
    #     self.vm.task().delete()

class test_OvfHandler(TestCase_OVA):
    def setUp(self) -> None:
        self.ova_handler = OvfHandler(self.ova_path)

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

class test_file_handle(TestCase_OVA):
    def setUp(self) -> None:
        self.filehandle=FileHandle(self.ova_path)
        self.ovfhandler=OvfHandler(self.ova_path)

    def test_init(self):
        assert self.filehandle is not None

    def test_tell(self):
        response=self.filehandle.tell()
        assert response is not None

    def test_seekable(self):
        response=self.filehandle.seekable()
        assert response is True

    def test_progress(self):
        self.filehandle.offset=self.filehandle.st_size/2
        response = self.filehandle.progress()
        assert response is 50

    def test_seek(self):
        response=self.filehandle.seek(offset=1,whence=0)
        assert response is 1

        expected = self.filehandle.offset + 1
        response=self.filehandle.seek(offset=1,whence=1)
        assert response is expected

        response = self.filehandle.seek(offset=1,whence=2)
        assert response is not None

class test_web_handle(TestCase_OVA):
    def setUp(self) -> None:
        self.ovfhandler=OvfHandler(self.url)
        self.webhandle=WebHandle(url=self.url)

    def test_init(self):
        assert self.webhandle is not None

    def test_tell(self):
        response=self.webhandle.tell()
        assert response is not None

    def test_seekable(self):
        response=self.webhandle.seekable()
        assert response is True

    def test_progress(self):
        self.webhandle.offset=self.webhandle.st_size/2
        response = self.webhandle.progress()
        assert response is 50

    def test_headers_to_dict(self):
        response = urlopen(self.url)
        response=self.webhandle._headers_to_dict(r=response)
        assert 'accept-ranges' in response

    def test_seek(self):
        response=self.webhandle.seek(offset=1,whence=0)
        assert response is 1

        expected = self.webhandle.offset +1
        response=self.webhandle.seek(offset=1,whence=1)
        assert response is expected

        response = self.webhandle.seek(offset=1,whence=2)
        assert response is not None