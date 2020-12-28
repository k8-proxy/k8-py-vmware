from pprint import pprint
from unittest import TestCase

from gw_proxy.src.VM_Server_Esxi_04 import VM_Server_Esxi_04
from k8_vmware.Config import Config
from k8_vmware.vsphere.Sdk import Sdk


class test_VM_Server_Esxi_04(TestCase):
    def setUp(self) -> None:
        self.vm_server = VM_Server_Esxi_04()
        print()

    def test__init__(self):
        assert 'esxi04' in self.vm_server.server_details['host']

    def test_list_vms(self):
        vm_names = self.vm_server.sdk.vms_names()
        assert 'icap-client' in vm_names

    def test_create_admin_user(self):
        user_id = "k8-vmware-tests"
        pprint(self.vm_server.create_admin_user(user_id))

    def test_user(self):
        sdk = Sdk()
        pprint(sdk.server_details())
        print(sdk.login())
