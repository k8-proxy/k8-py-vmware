import os

from osbot_utils.utils.Files import file_exists
from k8_vmware.helpers.TestCase_OVA import TestCase_OVA
from k8_vmware.vsphere.ova_utils.File_Handle import FileHandle
from k8_vmware.vsphere.ova_utils.OVA import OVA


class test_file_handle(TestCase_OVA):
    def setUp(self) -> None:
        self.ova = OVA()
        self.ova.download_ova_file(self.url, self.ova_path)
        self.filehandle = FileHandle(self.ova_path)

    def test_init(self):
        assert file_exists(self.ova_path)
        assert self.filehandle.filename is self.ova_path
        assert self.filehandle.offset is 0
        self.assertEqual(self.filehandle.st_size ,os.stat(self.ova_path).st_size)

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

        expected=self.filehandle.st_size-1
        response = self.filehandle.seek(offset=1,whence=2)
        self.assertEqual(response , self.filehandle.fh.seek(1, 2))
        self.assertEqual(self.filehandle.offset , expected)

    def test_read(self):
        amount=10000
        response=self.filehandle.read(amount=amount)
        self.assertEqual( len(response.decode("utf-8",errors='ignore')), 10000)

