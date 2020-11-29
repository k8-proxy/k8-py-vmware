from pprint import pprint
from k8_vmware.helpers.TestCase_VM import TestCase_VM
from k8_vmware.vsphere.VM_Task import VM_Task


class test_VM_Task(TestCase_VM):
    vm_name = f"tests__unit__" + __name__

    def setUp(self):
        self.sdk = self.temp_vm.sdk
        self.vm  = self.temp_vm.vm
        self.vm_task = VM_Task(sdk=self.sdk, vm=self.vm)

    def test__init__(self):
        assert self.vm_task.sdk == self.sdk
        assert self.vm_task.vm  == self.vm
        assert self.vm.name() == test_VM_Task.vm_name

# def power_on(self):
#     task = self.vm.PowerOnVM_Task()
#     return VM_Task(self.sdk).wait_for_task(task)
# def test_power_on(self):
#     print(self.vm.power_on())
#     pass
#     #pprint(self.vm.info())
#     #with Temp_VM() as vm:
#     #    print(vm.power_on())
