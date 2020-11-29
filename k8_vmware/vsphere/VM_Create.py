import pyVmomi
from osbot_utils.utils.Misc import random_string

from k8_vmware.vsphere.Sdk import Sdk
from k8_vmware.vsphere.Task import Task
from k8_vmware.vsphere.VM import VM


class VM_Create:
    def __init__(self, vm_name=None, data_store=None, guest_id=None):
        self.vm_name    : str = vm_name    or f"random_name_{random_string()}"
        self.data_store : str = data_store or 'datastore1'
        self.guest_id   : str = guest_id   or 'ubuntu64Guest'
        self.sdk        : Sdk = Sdk()
        self.vm         : VM  = None                                          # will have the VM object after creation

    def create(self):
        folder        = self.sdk.datacenter_folder()
        resource_pool = self.sdk.resource_pool()

        datastore_path = '[' + self.data_store + '] ' + self.vm_name

        # bare minimum VM shell, no disks. todo: add these as special options
        vmx_file = pyVmomi.vim.vm.FileInfo(logDirectory=None,
                                           snapshotDirectory=None,
                                           suspendDirectory=None,
                                           vmPathName=datastore_path)

        config = pyVmomi.vim.vm.ConfigSpec(name=self.vm_name, memoryMB=128, numCPUs=1,
                                           files=vmx_file, guestId=self.guest_id,
                                           version='vmx-07')

        task = folder.CreateVM_Task(config=config, pool=resource_pool)
        Task().wait_for_task(task)

        self.vm = VM(task.info.result)
        return self.vm

    def set_vm_name(self, vm_name):
        self.vm_name = vm_name
        return self