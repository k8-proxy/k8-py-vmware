import pyVmomi

from k8_vmware.vsphere.Sdk import Sdk
from k8_vmware.vsphere.Task import Task


class VM_Device:
    def __init__(self, vm):
        self.sdk            = Sdk()
        self.vm             = vm

    def disk_get_available_unit_number(self):
        unit_number = 0
        for dev in  self.vm.devices():
            if hasattr(dev.backing, 'fileName'):
                unit_number = int(dev.unitNumber) + 1
                if unit_number == 7:        # unit_number 7 reserved for scsi controller
                    unit_number += 1
                if unit_number >= 16:
                    raise Exception("[disk_get_available_unit_number] Unit Number was bigger than 16")
        return unit_number

    def disk_get_scsi_controller(self):
        controllers = self.vm.devices_SCSI_Controllers()
        if len(controllers) == 0:
            raise Exception("[disk_get_scsi_controller] no SCSI controllers available")
        return controllers.pop()

    def disk_ide_add_to_vm(self, disk_size, disk_type="thin"):      # for what disk_type="thin" means see https://docs.vmware.com/en/VMware-vSphere/6.7/com.vmware.vsphere.storage.doc/GUID-8204A8D7-25B6-4DE2-A227-408C158A31DE.html
        ide_controller = self.vm.controller_ide()
        return self.disk_add_to_vm(disk_size, ide_controller, disk_type)

    def disk_scsi_add_to_vm(self, disk_size, disk_type="thin"):
        scsi_controller = self.vm.controller_scsi()
        return self.disk_add_to_vm(disk_size, scsi_controller, disk_type)

    def disk_add_to_vm(self, disk_size, controller, disk_type=None):
        unit_number                         = self.disk_get_available_unit_number()
        new_disk_kb                         = int(disk_size) * 1024 * 1024
        disk_spec                           = pyVmomi.vim.vm.device.VirtualDeviceSpec()
        disk_spec.fileOperation             = "create"
        disk_spec.operation                 = pyVmomi.vim.vm.device.VirtualDeviceSpec.Operation.add
        disk_spec.device                    = pyVmomi.vim.vm.device.VirtualDisk()
        disk_spec.device.backing            = pyVmomi.vim.vm.device.VirtualDisk.FlatVer2BackingInfo()
        disk_spec.device.backing.diskMode   = 'persistent'
        disk_spec.device.unitNumber         = unit_number
        disk_spec.device.capacityInKB       = new_disk_kb
        disk_spec.device.controllerKey      = controller.key
        if disk_type == 'thin':
            disk_spec.device.backing.thinProvisioned = True
        return self.reconfig_vm(disk_spec)

    def disk_delete(self, disk):
        disk_path   = disk.backing.fileName
        diskManager = self.sdk.content().virtualDiskManager
        task        = diskManager.DeleteVirtualDisk_Task(name=disk_path, datacenter=self.sdk.datacenter())
        Task().wait_for_task(task)



    def scsi_controller__add_to_vm(self):
        scsi_spec                                = pyVmomi.vim.vm.device.VirtualDeviceSpec()
        scsi_spec.operation                      = pyVmomi.vim.vm.device.VirtualDeviceSpec.Operation.add
        scsi_spec.device                         = pyVmomi.vim.vm.device.ParaVirtualSCSIController()
        scsi_spec.device.deviceInfo              = pyVmomi.vim.Description()
        scsi_spec.device.slotInfo                = pyVmomi.vim.vm.device.VirtualDevice.PciBusSlotInfo()
        scsi_spec.device.slotInfo.pciSlotNumber  = 16
        scsi_spec.device.controllerKey           = 100
        scsi_spec.device.unitNumber              = 3
        scsi_spec.device.busNumber               = 0
        scsi_spec.device.hotAddRemove            = True
        scsi_spec.device.sharedBus               = 'noSharing'
        scsi_spec.device.scsiCtlrUnitNumber      = 7        
        self.reconfig_vm(scsi_spec)

    def reconfig_vm(self, device_spec):
        dev_changes = []
        spec        = pyVmomi.vim.vm.ConfigSpec()
        dev_changes.append(device_spec)
        spec.deviceChange = dev_changes
        task        = self.vm.vm.ReconfigVM_Task(spec=spec)
        Task().wait_for_task(task)
        return task

    def remove_device(self, device):
        device_spec           = pyVmomi.vim.vm.device.VirtualDeviceSpec()
        device_spec.operation = pyVmomi.vim.vm.device.VirtualDeviceSpec.Operation.remove
        device_spec.device    = device
        config_spec           = pyVmomi.vim.vm.ConfigSpec()
        config_spec.deviceChange.append(device_spec)
        task = self.vm.vm.ReconfigVM_Task(spec=config_spec)
        Task().wait_for_task(task)                          #todo: add check if device is still in there (there are cases when it seems like the removal fails, but no errors are shown (for example when removing an SCSI controller that has disks associated with))
