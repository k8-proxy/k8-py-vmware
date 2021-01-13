from pprint import pprint
from unittest import TestCase

from osbot_utils.utils.Misc import random_string

from k8_vmware.helpers.Temp_VM import Temp_VM
from k8_vmware.vsphere.Sdk import Sdk


class test_Temp_VM(TestCase):

    def setUp(self):
        self.temp_vm = Temp_VM()

    def test__init__(self):
        assert "unit_tests__temp_vm_" in self.temp_vm.vm_name

    def test_create__delete(self):
        vm = self.temp_vm.create()
        assert self.temp_vm.vm      == vm
        assert self.temp_vm.vm_name == vm.name()

        delete_task = self.temp_vm.delete()
        assert delete_task.info.state == "success"

    def test____enter____exit__(self):
        sdk = Sdk()
        vm_name = f"test____enter____exit__{random_string()}"
        with Temp_VM(vm_name) as vm:
            assert vm.name() == vm_name
            assert sdk.find_by_name(vm_name).name() == vm_name      # search VM and confirm it is there

        assert sdk.find_by_name(vm_name) == None                    # search outsite the `with` statement and confirm that is NOT there