from unittest import TestCase

from k8_vmware.helpers.Temp_VM import Temp_VM


class TestCase_VM(TestCase):
    vm_name = "tests__unit__vsphere__test_VM_Task"
    temp_vm = None

    @classmethod
    def setUpClass(cls) -> None:
        vm_name = cls.vm_name or TestCase_VM.vm_name
        TestCase_VM.temp_vm = Temp_VM(vm_name=vm_name)
        TestCase_VM.temp_vm.create()

    @classmethod
    def tearDownClass(cls) -> None:
        TestCase_VM.temp_vm.delete()