from unittest import TestCase

from k8_vmware.helpers.Temp_VM import Temp_VM
from k8_vmware.vsphere.Sdk import Sdk
from k8_vmware.vsphere.VM import VM


class TestCase_VM(TestCase):
    vm_name = "tests__unit__vsphere__test_VM_Task"
    temp_vm = None

    @classmethod
    def setUpClass(cls) -> None:
        vm_name     : str     = cls.vm_name or cls.vm_name
        cls.temp_vm : Temp_VM = Temp_VM(vm_name=vm_name)
        cls.sdk     : Sdk     = cls.temp_vm.sdk
        cls.vm      : VM      = cls.temp_vm.create()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp_vm.delete()