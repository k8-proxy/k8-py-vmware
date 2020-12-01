import pyVmomi
from osbot_utils.utils.Misc import random_string

from k8_vmware.vsphere.Sdk import Sdk
from k8_vmware.vsphere.Task import Task
from k8_vmware.vsphere.VM import VM


class VM_Create:
    def __init__(self, vm_name=None, data_store=None, guest_id=None):
        self.vm_name    : str  = vm_name    or f"random_name_{random_string()}"
        self.data_store : str  = data_store or 'datastore1'
        self.guest_id   : str  = guest_id   or 'ubuntu64Guest'
        self.sdk        : Sdk  = Sdk()
        self.vm         : VM   = None                                          # will have the VM object after creation
        self.devices    : list = []

    def add_device__nic(self, network):
        nicspec                                      = pyVmomi.vim.vm.device.VirtualDeviceSpec()
        nic_type                                     = pyVmomi.vim.vm.device.VirtualVmxnet3()
        nicspec.operation                            = pyVmomi.vim.vm.device.VirtualDeviceSpec.Operation.add
        nicspec.device                               = nic_type
        nicspec.device.deviceInfo                    = pyVmomi.vim.Description()
        nicspec.device.backing                       = pyVmomi.vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
        nicspec.device.backing.network               = network
        nicspec.device.backing.deviceName            = network.name
        nicspec.device.connectable                   = pyVmomi.vim.vm.device.VirtualDevice.ConnectInfo()
        nicspec.device.connectable.startConnected    = True
        nicspec.device.connectable.allowGuestControl = True
        self.devices.append(nicspec)
        return self

    #     nicspec = pyVmomi.vim.vm.device.VirtualDeviceSpec()
    #     nicspec.operation = pyVmomi.vim.vm.device.VirtualDeviceSpec.Operation.add
    #     nic_type = pyVmomi.vim.vm.device.VirtualVmxnet3()
    #     nicspec.device = nic_type
    #     nicspec.device.deviceInfo = pyVmomi.vim.Description()
    #     nicspec.device.backing = pyVmomi.vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
    #     nicspec.device.backing.network = net_name
    #     nicspec.device.backing.deviceName = net_name.name
    #     nicspec.device.connectable = pyVmomi.vim.vm.device.VirtualDevice.ConnectInfo()
    #     nicspec.device.connectable.startConnected = True
    #     nicspec.device.connectable.allowGuestControl = True
    #     devices.append(nicspec)


    def create(self):
        folder        = self.sdk.datacenter_folder()
        resource_pool = self.sdk.resource_pool()

        datastore_path = '[' + self.data_store + '] ' #+ self.vm_name  # add "self.vm_name" here (as seen in samples) was creating an extra folder and was leaving a folder behind

        vmx_file = self.sdk.file_info(vm_path_name=datastore_path)
        # todo :refactor these values below
        config = pyVmomi.vim.vm.ConfigSpec(name         = self.vm_name  ,
                                           memoryMB     = 128           ,
                                           numCPUs      = 1             ,
                                           files        = vmx_file      ,
                                           guestId      = self.guest_id ,
                                           version      = 'vmx-07'      ,
                                           deviceChange = self.devices  )

        task = folder.CreateVM_Task(config=config, pool=resource_pool)
        Task().wait_for_task(task)

        self.vm = VM(task.info.result)
        return self.vm

    def set_vm_name(self, vm_name):
        self.vm_name = vm_name
        return self