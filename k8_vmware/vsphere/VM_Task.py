import pyVmomi

from k8_vmware.vsphere.Datastore import Datastore
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
                self.power_off()
            vm_name = self.vm.name()                    # capture the vm_name
            task_destroy = self.vm.vm.Destroy_Task()    # delete the vm
            Task().wait_for_task(task_destroy)          # wait until deletion is done
            #Datastore().folder_delete(vm_name)          # todo remove this line once confirmed there are no side effects (not neeeded any more) delete folder created by VM
            return task_destroy


    # def delete__by_name(self, vm_name : str):
    #     vm = self.sdk.find_by_name(vm_name)
    #     return self.delete(vm)

    def power_on(self):
        if not self.vm.powered_on():
            task = self.vm.vm.PowerOnVM_Task()              # todo refactor into task API
            return Task().wait_for_task(task)

    def power_off(self):
        task = self.vm.vm.PowerOffVM_Task()
        return Task().wait_for_task(task)