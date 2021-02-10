from k8_vmware.helpers.TestCase_OVA import TestCase_OVA
from k8_vmware.vsphere.ova_utils.OVF_Handler import Ovf_Hanlder
from k8_vmware.vsphere.ova_utils.Web_Handle import Web_Handle

class test_web_handle(TestCase_OVA):
    def setUp(self) -> None:
        self.ovfhandler  =  Ovf_Hanlder(self.url)
        self.webhandle   =  Web_Handle(url=self.url)

    def test_init(self):
        assert self.webhandle.url is self.url
        assert self.webhandle.offset is 0

    def test_tell(self):
        self.webhandle.offset = 50
        response  = self.webhandle.tell()
        assert response is 50

    def test_seekable(self):
        response  = self.webhandle.seekable()
        assert response is True

    def test_progress(self):
        self.webhandle.offset=self.webhandle.st_size/2
        response  = self.webhandle.progress()
        assert response is 50

    def test_seek(self):
        response  = self.webhandle.seek(offset=1,whence=0)
        assert response is 1

        expected  =  self.webhandle.offset + 1
        response  =  self.webhandle.seek(offset=1,whence=1)
        assert response is expected

        expected  =  self.webhandle.st_size - 1
        response  =  self.webhandle.seek(offset=1,whence=2)
        self.assertEqual(response, expected)
