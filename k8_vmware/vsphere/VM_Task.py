import pyVmomi

from k8_vmware.vsphere.Sdk import Sdk
from k8_vmware.vsphere.Task import Task
from k8_vmware.vsphere.VM import VM


# See list of tasks here https://code.vmware.com/apis/968 (click on "All Methods" and search for _Task)

class VM_Task:
    def __init__(self, vm : VM):
        self.sdk = Sdk()
        self.vm = vm

    def delete(self):
        if self.vm:
            if self.vm.powered_on():
                # todo: add power off task
                pass
            task_destroy = self.vm.vm.Destroy_Task()
            return Task().wait_for_task(task_destroy)

    def delete__by_name(self, vm_name : str):
        vm = self.sdk.find_by_name(vm_name)
        return self.delete(vm)

    def power_on(self):
        task = self.vm.vm.PowerOnVM_Task()              # todo refactor into task API
        return Task().wait_for_task(task)

    def power_off(self):
        task = self.vm.vm.PowerOffVM_Task()
        return Task().wait_for_task(task)