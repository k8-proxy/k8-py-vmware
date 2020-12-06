from unittest import TestCase

from osbot_utils.utils.Files import file_exists

from gw_proxy.src.utils.Tiny_Core_Linux import Tiny_Core_Linux
from k8_vmware.helpers.View_Soap_Calls import View_Soap_Calls


class test_Tiny_Core_Linux(TestCase):

    def setUp(self):
        self.build = Tiny_Core_Linux()

    def test_create_vm(self):
        print()
        with View_Soap_Calls():
            print(self.build.create_vm())

    def test_download_iso(self):
        assert file_exists(self.build.download_iso())


