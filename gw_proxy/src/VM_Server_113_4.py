from k8_vmware.Config import Config
from k8_vmware.vsphere.Network import Network
from k8_vmware.vsphere.Sdk import Sdk
from k8_vmware.vsphere.VM_Process import VM_Process


class VM_Server_113_4:

    def __init__(self):
        self.sdk            = Sdk()
        self.network        = Network()
        self.server_details = Config().vsphere_server_details()

        # settings
        self.vswitch_name    = 'vSwitch0'
        self.port_group_name = 'VM'

    def settings__check(self):
        switches = self.network.virtual_switches()
        assert len(switches)    == 1                            # there should only be one virtual switch
        assert switches[0].name == self.vswitch_name            # confirm expected name

    def setup_network(self):
        if self.port_group_name not in self.network.networks_names():
            self.network.port_group_create(self.port_group_name, self.vswitch_name)

    def setup_network__check(self):
        assert self.port_group_name in self.network.networks_names()




    # misc vm tests

    def minio_test_setup_network(self):
        vm = self.sdk.find_by_name("test-vm-from-ovf")
        vm_process = VM_Process(vm)
        #print(vm_process.exec('/bin/ip', 'a'))
        #print(vm_process.exec('/bin/ip', 'addr add 10.102.66.200/24 dev enp0s25'))
        #print(vm_process.exec('/bin/cat', '/etc/shadow'))
        #print(vm_process.exec('/bin/bash', '-c "sudo /bin/cat /etc/shadow"'))
        print(vm_process.exec('/bin/bash', '-c "sudo ip addr add 78.159.113.32/26 dev eth0"')) # commands from https://ubuntu.com/server/docs/network-configuration
        print(vm_process.exec('/bin/bash', '-c "sudo ip route add default via 78.159.113.62"'))

        print(vm_process.exec('/bin/ip', 'a'))
        print(vm_process.exec('/bin/ip', 'route show'))


