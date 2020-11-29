from k8_vmware.vsphere.Task import Task
from k8_vmware.vsphere.VM import VM


class VM_Task:
    def __init__(self, sdk, vm : VM):
        self.sdk = sdk
        self.vm = vm

    def power_on(self):
        task = self.vm.vm.PowerOnVM_Task()
        return Task(self.sdk).wait_for_task(task)

    def power_off(self):
        task = self.vm.vm.PowerOffVM_Task()
        return Task(self.sdk).wait_for_task(task)