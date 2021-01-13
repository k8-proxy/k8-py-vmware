import pyVmomi

from k8_vmware.helpers.TestCase_VM import TestCase_VM
from k8_vmware.vsphere.VM import VM


class test_TestCase_VM(TestCase_VM):

    def test_setUpClass(self):
        assert type(self.vm   ) == VM
        assert type(self.vm.vm) == pyVmomi.vim.VirtualMachine
        assert self.vm.name(  ) == self.vm_name