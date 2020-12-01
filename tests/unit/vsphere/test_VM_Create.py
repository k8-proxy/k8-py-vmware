from pprint import pprint
from unittest import TestCase

import pyVmomi

from k8_vmware.vsphere.Network import Network
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

        vswitch      = 'vSwitch0'
        network_name = 'temp_network-2'
        network      = self.get_test_network(network_name, vswitch)

        self.vm_create.add_device__nic(network)
        vm = self.vm_create.create()
        print(vm)
        vm.task().power_on()
        vm.task().delete()

        self.delete_test_network(network_name)

