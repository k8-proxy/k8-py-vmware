from k8_vmware.helpers.TestCase_VM import TestCase_VM
from k8_vmware.vsphere.VM_Device import VM_Device

class test_VM_Device(TestCase_VM):
    vm_name = f"tests__unit__" + __name__

    def setUp(self) -> None:
        self.vm_name = test_VM_Device.vm_name
        self.vm_device = VM_Device(vm=self.vm)

    def test_disk_add_to_vm(self):
        disk_1_size = 10
        disk_2_size = 10
        assert self.vm_device.vm.controller_scsi() is None
        assert len(self.vm_device.vm.devices()      ) == 9
        assert len(self.vm_device.vm.devices_Disks()) == 0

        self.vm_device.scsi_controller__add_to_vm()                 # add scsi controller
        self.vm_device.disk_add_to_vm(disk_1_size)
        self.vm_device.disk_add_to_vm(disk_2_size)

        disks= self.vm_device.vm.devices_Disks()

        assert disks[0].capacityInBytes == disk_1_size * 1024 * 1024 * 1024
        assert disks[1].capacityInBytes == disk_1_size * 1024 * 1024 * 1024
        assert len(self.vm_device.vm.devices()) == 12

        controller_scsi = self.vm_device.vm.controller_scsi()

        self.vm_device.remove_device(disks[0])
        self.vm_device.remove_device(disks[1])
        self.vm_device.remove_device(controller_scsi)

        assert len(self.vm_device.vm.devices()      ) == 9
        assert len(self.vm_device.vm.devices_Disks()) == 0
        assert self.vm_device.vm.controller_scsi() is None


    def test_scsi_controller__add_to_vm(self):
        assert len(self.vm_device.vm.devices()) == 9
        assert self.vm_device.vm.controller_scsi() is None

        self.vm_device.scsi_controller__add_to_vm()

        scsi_controller = self.vm_device.vm.controller_scsi()
        assert scsi_controller.deviceInfo.label == 'SCSI controller 0'
        assert len(self.vm_device.vm.devices()) == 10

        self.vm_device.remove_device(scsi_controller)

        assert self.vm_device.vm.controller_scsi() == None
        assert len(self.vm_device.vm.devices()) == 9
