from pprint import pprint
from unittest import TestCase

from k8_vmware.helpers.Test_VMs import Test_VMs


class test_Test_VMs(TestCase):

    def setUp(self):
        self.test_vms = Test_VMs()

    def test__init__(self):
        assert self.test_vms.test_vm_name is "unit_tests_vm"

    def test_create_test_vm(self):
        pprint(self.test_vms.sdk.vms_names())
        pass
