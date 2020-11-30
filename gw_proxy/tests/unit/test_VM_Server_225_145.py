from pprint import pprint
from unittest import TestCase

from gw_proxy.src.VM_Server_225_145 import VM_Server_225_145
from k8_vmware.vsphere.VM_Process import VM_Process


class test_VM_Server_225_145(TestCase):

    def setUp(self) -> None:
        self.vm_server = VM_Server_225_145()
        print()

    def test__init__(self):
        assert '225.145' in self.vm_server.server_details['host']
        assert self.vm_server.sdk.find_by_name(self.vm_server.vm_name__minio_test) is not None

    def test_minio_test_setup_network(self):
        result = self.vm_server.minio_test_setup_network()
        print(result)

    def test_minio_test_get_request(self):
        result = self.vm_server.minio_test_get_request()
        print(result)
        vm = self.vm_server.sdk.find_by_name(self.vm_server.vm_name__minio_test)
        vm_process = VM_Process(vm)
        pprint(vm_process.curl('http://91.109.26.22'))

    def test_minio_test_vm_power_off(self):
        pprint(self.vm_server.minio_test_vm_power_off())
