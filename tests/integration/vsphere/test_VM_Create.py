from pprint import pprint
from unittest import TestCase

import pyVmomi

from k8_vmware.vsphere.Network import Network
from k8_vmware.vsphere.Sdk import Sdk
from k8_vmware.vsphere.Task import Task
from k8_vmware.vsphere.VM import VM
from k8_vmware.vsphere.VM_Create import VM_Create


class test_VM_Create(TestCase):
    def setUp(self) -> None:
        self.vm_create = VM_Create()

    def test__init__(self):
        assert 'random_name_' in self.vm_create.vm_name
        assert self.vm_create.data_store == 'datastore1'
        assert self.vm_create.guest_id   == 'ubuntu64Guest'

    def test_vm_create__delete(self):
        print()
        vm               = self.vm_create.create()
        assert vm.name() == self.vm_create.vm_name

        task_delete     = vm.task().delete()
        assert task_delete.info.state == "success"

    def get_test_network(self, network_name, vswitch):
        network = Network()
        if network.port_group_not_exists(network_name):
            return network.port_group_create(network_name, vswitch)
        return network.sdk.get_object_network(network_name)

    def delete_test_network(self, network_name):
        network = Network()
        if network.port_group_exists(network_name):
            network.port_group_delete(network_name)

    def test_create_vm_with_network(self):
        vm_name      = self.vm_create.vm_name
        disk_size    = 10
        vswitch      = 'vSwitch0'
        network_name = 'temp_network-2'
        network      = self.get_test_network(network_name, vswitch)

        self.vm_create.add_device__nic(network)
        scsi_ctr = self.vm_create.add_device__scsi()
        self.vm_create.add_device__disk(disk_size, vm_name, scsi_ctr)
        vm = self.vm_create.create()
        vm.task().delete()

        self.delete_test_network(network_name)


    # def test_cdrom(self):
    #     iso_path = ''
    #     cdrom_type = 'client'
    #     vm_name = "random_name_JCKFSL"
    #     sdk = Sdk()
    #     vm = sdk.vm(vm_name)
    #
    #     #result = self.vm_create.get_vm_cdrom_devices()
    #     print()
    #
    #     ide_devices = vm.devices_Virtual_IDE_Controllers()
    #     ide_device = ide_devices[0]             # pick the first one
    #     assert len(ide_device.device) < 4       # make sure there is space to add CDRom
    #
    #     cdrom_spec =self.vm_create.add_device_cdrom(ide_device, cdrom_type)
    #
    #     #self.configspec = pyVmomi.vim.vm.ConfigSpec()
    #     #pprint(cdrom_spec)
    #     #self.configspec.deviceChange.append(cdrom_spec)
    #     #task = vm.vm.ReconfigVM_Task(spec=self.configspec)
    #     #Task().wait_for_task(task)
    #
    #     cdrom_spec = self.device_helper.remove_cdrom(cdrom_device)
    #     self.change_detected = True
    #     self.configspec.deviceChange.append(cdrom_spec)
    #
    #     cd_rom_devices = vm.devices_Virtual_Cdroms()
    #     pprint(cd_rom_devices)

