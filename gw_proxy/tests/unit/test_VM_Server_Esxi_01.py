from pprint import pprint
from unittest import TestCase

from gw_proxy.src.VM_Server_Esxi_01 import VM_Server_Esxi_01
from k8_vmware.helpers.Sdk_User import Sdk_User


class test_VM_Server_Esxi_01(TestCase):
    def setUp(self) -> None:
        self.vm_server = VM_Server_Esxi_01()
        print()

    def test__init__(self):
        assert 'esxi01' in self.vm_server.server_details['host']

    def test_list_vms(self):
        vm_names = self.vm_server.sdk.vms_names()
        assert 'centos-testing' in vm_names

    def test_ssh_execution(self):
        assert self.vm_server.esx_cli.esxi_ssh.exec('uname') == 'VMkernel'

    def test_list_users(self):
        users = self.vm_server.esx_cli.system_account_list(index_by='UserID')
        assert 'root' in users

    def test_create_admin_user(self):
        user_id = "guest-account"
        result = self.vm_server.create_admin_user(user_id)
        pprint(result)
        assert user_id in set(self.vm_server.esx_cli.system_account_list(index_by='UserID'))
        with Sdk_User(user_id=result['user_id'], password=result['password']) as sdk_user:                                # login to server with the temp user
            assert sdk_user.login_result is True



    #def test_user(self):
    #    sdk = Sdk()
    #    pprint(sdk.server_details())
    #    print(sdk.login())
