from unittest import TestCase

from k8_vmware.Config import Config
from k8_vmware.helpers.Debug import Debug
from k8_vmware.helpers.View_Soap_Calls import View_Soap_Calls


class test_Config(TestCase):

    def setUp(self) -> None:
        self.config = Config()

    def test_vsphere_server(self):
        server_details = self.config.vsphere_server_details()
        assert server_details.get('host'    ) is not None
        assert server_details.get('username') is not None
        assert server_details.get('password') is not None

    def test_vm_account(self):
        vm_account = self.config.vm_account()
        assert vm_account.get('username') is not None
        assert vm_account.get('password') is not None
