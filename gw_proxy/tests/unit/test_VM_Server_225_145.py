from unittest import TestCase

from gw_proxy.src.VM_Server_225_145 import VM_Server_225_145


class test_VM_Server_225_145(TestCase):

    def setUp(self) -> None:
        self.vm_server = VM_Server_225_145()

    def test__init__(self):
        assert '225.145' in self.vm_server.server_details['host']
        assert self.vm_server.sdk.find_by_name(self.vm_server.vm_name__minio_test) is not None

    def test_minio_test_setup_network(self):
        print()
        result = self.vm_server.minio_test_setup_network()
        print(result)