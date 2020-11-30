import requests

from k8_vmware.Config import Config
from k8_vmware.vsphere.Sdk import Sdk
from k8_vmware.vsphere.VM_Process import VM_Process


class VM_Server_225_145:

    def __init__(self):
        self.sdk = Sdk()
        self.server_details = Config().vsphere_server_details()
        self.vm_name__minio_test = 'dinis-test-via-ovf'

    def minio_test_setup_network(self):
        vm = self.sdk.find_by_name(self.vm_name__minio_test)
        vm_process = VM_Process(vm)
        #print(vm_process.exec('/bin/ip', 'a'))
        #print(vm_process.exec('/bin/ip', 'addr add 10.102.66.200/24 dev enp0s25'))
        #print(vm_process.exec('/bin/cat', '/etc/shadow'))
        #print(vm_process.exec('/bin/bash', '-c "sudo /bin/cat /etc/shadow"'))
        print(vm_process.exec('/bin/bash', '-c "sudo ip addr add 91.109.26.22/27 dev eth0"')) # commands from https://ubuntu.com/server/docs/network-configuration
        print(vm_process.exec('/bin/bash', '-c "sudo ip route add default via 91.109.26.30"'))

        print(vm_process.exec('/bin/ip', 'a'))
        print(vm_process.exec('/bin/ip', 'route show'))

    def minio_test_get_request(self):
        resp = requests.get('http://91.109.26.22')
        return resp.text

    def minio_test_vm_power_off(self):
        vm = self.sdk.find_by_name(self.vm_name__minio_test)
        vm.task().power_off()
        return vm.info()




