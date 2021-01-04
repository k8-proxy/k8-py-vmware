from unittest import TestCase

from osbot_utils.utils.Files import file_exists

from gw_proxy.src.utils.Tiny_Core_Linux import Tiny_Core_Linux
from k8_vmware.helpers.for_osbot_utils.Wrap_Method import Wrap_Method


def before_call(*args , **kvargs):
    info = args[2]
    _args = args[3]
    print('---------------------------')
    print(f"[SOAP-CALL] {info.wsdlName:30} : {info.methodResultName}")  # DC use this to see the calls made via the /SDK
    print(_args)
    print('---------------------------')
    return (args, kvargs)

class test_Tiny_Core_Linux(TestCase):

    def setUp(self):
        self.build = Tiny_Core_Linux()

    def test_create_vm(self):
        print()
        #with View_Soap_Calls():
        from pyVmomi import SoapAdapter
        self.wrap_method = Wrap_Method(SoapAdapter.SoapStubAdapter, "InvokeMethod")
        self.wrap_method.add_on_before_call(before_call)
        with self.wrap_method:
            print(self.build.create_vm())

    def test_download_iso(self):
        assert file_exists(self.build.download_iso())


