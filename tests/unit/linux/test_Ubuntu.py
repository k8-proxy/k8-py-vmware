from unittest import TestCase

import pyVmomi

from k8_vmware.helpers.View_Soap_Calls import View_Soap_Calls
from k8_vmware.linux.Ubuntu import Ubuntu
from k8_vmware.vsphere.VM_Create import VM_Create


class test_Ubuntu(TestCase):

    def setUp(self) -> None:
        self.vm_create = VM_Create()
        self.vm = self.vm_create.create()
        self.vm_name = self.vm_create.vm_name
        self.ubuntu = Ubuntu(self.vm_name)

    def tearDown(self) -> None:
        self.vm.task().delete()

    def test__init__(self):
        assert self.ubuntu.vm_name == self.vm_name

    def test_vm(self):
        with View_Soap_Calls():
            assert self.ubuntu.vm().name() == self.vm_name

    def test_query(self):
        sdk = self.ubuntu.sdk
        vm = sdk.get_object(pyVmomi.vim.VirtualMachine, self.vm_name)
        assert vm.name == self.vm_name

        properties = ['parent', 'configStatus', 'config', 'tag']
        with View_Soap_Calls(show_calls=True, show_xml=False):
            result = sdk.get_objects_properties(pyVmomi.vim.VirtualMachine, [vm], properties)
            self.assertIsNotNone(result.get(self.vm.id()).get("config"))
            self.assertIsNotNone(result.get(self.vm.id()).get("parent"))
            self.assertIsNotNone(result.get(self.vm.id()).get("configStatus"))
            self.assertIsNotNone(result.get(self.vm.id()).get("tag"))
