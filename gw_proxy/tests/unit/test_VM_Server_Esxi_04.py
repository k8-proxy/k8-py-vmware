from pprint import pprint
from unittest import TestCase

from gw_proxy.src.VM_Server_Esxi_04 import VM_Server_Esxi_04
from k8_vmware.Config import Config
from k8_vmware.helpers.Sdk_User import Sdk_User
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
        result = self.vm_server.create_admin_user(user_id)
        assert user_id in set(self.vm_server.esx_cli.system_account_list(index_by='UserID'))
        with Sdk_User(user_id=result['user_id'], password=result['password']) as sdk_user:                                # login to server with the temp user
            assert sdk_user.login_result is True
        pprint(result)


    #def test_user(self):
    #    sdk = Sdk()
    #    pprint(sdk.server_details())
    #    print(sdk.login())
