from pprint import pprint
from unittest import TestCase

import pyVmomi
from osbot_utils.utils.Misc import random_string

from k8_vmware.vsphere.Network import Network


class test_Network(TestCase):

    def setUp(self) -> None:
        self.network = Network()


    def test_networks(self):
        networks = self.network.networks()

        print()
        pprint(type(networks))

    def test_port_group_create__port_group_delete(self):
        name         = 'temp_port_group_' + random_string()                         # temp port_group to created
        vswitch_name = 'vSwitch0'                                                   # default vswitch name
        network      = self.network.port_group_create(name, vswitch_name)           # create port_group
        assert network.name == name                                                 # confirm we received an object with the newly created network
        assert name in self.network.networks_names()                                # confirm it exists
        self.network.port_group_delete(name)                                        # delete port_group
        assert name not in self.network.networks_names()                            # confirm it has been deleted


    def test_virtual_switches(self):
        switches = self.network.virtual_switches()
        assert len(switches) ==1
        assert switches[0].name == 'vSwitch0'
        assert switches[0].spec.bridge.nicDevice == ['vmnic0']

    # def test_add_network(self):
    #     import pyVmomi
    #     from pprint import pprint
    #     from k8_vmware.vsphere.Sdk import Sdk
    #     print()
    #
    #     sdk = Sdk()
    #     networks = sdk.get_objects(pyVmomi.vim.Network)
    #     pprint(networks[0])
    #     return
    #
    #
    #
    #     vm_name = "Controller"
    #     vm = sdk.find_by_name(vm_name)
    #
    #     pprint(vm.devices_indexed_by_label()['Network adapter 1'])
    #     # with View_Soap_Calls(show_xml=False, show_calls=False):
    #     #     hardware = vm.vm.config.hardware
    #     #     device = hardware.device
    #     #     for device in hardware.device:
    #     #         pprint(device.deviceInfo.label)
    #
    #         # vim.Network:HaNetwork-VMs




