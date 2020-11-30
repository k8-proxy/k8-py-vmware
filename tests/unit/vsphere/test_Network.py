from pprint import pprint
from unittest import TestCase

import pyVmomi

from k8_vmware.vsphere.Network import Network


class test_Network(TestCase):

    def setUp(self) -> None:
        self.network = Network()

    def test_list(self):
        networks = self.network.list()

        print()
        pprint(networks)

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




