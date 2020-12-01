from pprint import pprint
from unittest import TestCase

from gw_proxy.src.VM_Server_113_4 import VM_Server_113_4

from k8_vmware.vsphere.VM_Process import VM_Process


class test_VM_Server_113_4(TestCase):

    def setUp(self) -> None:
        self.vm_server = VM_Server_113_4()
        print()

    def test__init__(self):
        assert '113.4' in self.vm_server.server_details['host']

    def test_settings__check(self):
        self.vm_server.settings__check()

    def test_setup_network(self):
        self.vm_server.setup_network()
        self.vm_server.setup_network__check()



    # Ubuntu VM tests

    def test_create_ubuntu_vm(self):
        self.vm_server.create_ubuntu_vm()

    def test_ubuntu_vm_run_commands(self):
        self.vm_server.ubuntu_vm_run_commands()

    # misc vm tests

    def test_minio_test_setup_network(self):
        self.vm_server.minio_test_setup_network()