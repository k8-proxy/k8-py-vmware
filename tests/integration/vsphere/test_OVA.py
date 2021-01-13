from unittest import TestCase
import os
from urllib.request import urlopen
from k8_vmware.vsphere.OVA import OVA, OvfHandler, FileHandle, WebHandle
from k8_vmware.vsphere.Sdk import Sdk
import wget

class test_OVA(TestCase):
    def setUp(self) -> None:
        self.ova = OVA()

    def test__init__(self):
        assert self.ova.sdk is not None

    def test_upload_ova_file(self):
        sdk=Sdk()
        if not os.path.exists('./test.ova'):
            url = "https://packages.vmware.com/photon/4.0/Beta/ova/photon-hw11-4.0-d98e681.ova"
            wget.download(url, './test.ova')
        ova_path="./test.ova"
        self.ova.upload_ova(ova_path)
        self.vm = sdk.find_by_name("Photon OS")
        print(self.vm)
        self.vm.task().delete()

    # def test_upload_ova_web(self):
    #     sdk=Sdk()
    #     url = "https://packages.vmware.com/photon/4.0/Beta/ova/photon-hw11-4.0-d98e681.ova"
    #     self.ova.upload_ova(url)
    #     self.vm = sdk.find_by_name("Photon OS")
    #     print(self.vm)
    #     self.vm.task().delete()

class test_OvfHandler(TestCase):
    def setUp(self) -> None:
        self.ova_path="./test.ova"
        self.ova_handler = OvfHandler(self.ova_path)
        self.url="https://packages.vmware.com/photon/4.0/Beta/ova/photon-hw11-4.0-d98e681.ova"

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

class test_file_handle(TestCase):
    def setUp(self) -> None:
        self.file = "./test.ova"
        self.filehandle=FileHandle(self.file)
        self.ovfhandler=OvfHandler(self.file)

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
        r=self.filehandle.seek(offset=1,whence=0)
        assert r is 1

        expected = self.filehandle.offset + 1
        r=self.filehandle.seek(offset=1,whence=1)
        assert r is expected

        r = self.filehandle.seek(offset=1,whence=2)
        assert r is not None

class test_web_handle(TestCase):
    def setUp(self) -> None:
        self.url = "https://packages.vmware.com/photon/4.0/Beta/ova/photon-hw11-4.0-d98e681.ova"
        self.webhandle=WebHandle(url=self.url)
        self.ovfhandler=OvfHandler(self.url)

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
        r = urlopen(self.url)
        response=self.webhandle._headers_to_dict(r=r)
        assert 'accept-ranges' in response

    def test_seek(self):
        r=self.webhandle.seek(offset=1,whence=0)
        assert r is 1

        expected = self.webhandle.offset +1
        r=self.webhandle.seek(offset=1,whence=1)
        assert r is expected

        r = self.webhandle.seek(offset=1,whence=2)
        assert r is not None

    def tearDown(self) -> None:
        if os.path.exists('./test.ova'):
            os.remove('./test.ova')
