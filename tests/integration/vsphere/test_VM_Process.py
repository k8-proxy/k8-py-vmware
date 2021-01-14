from os import environ

import pytest
from unittest import TestCase
from k8_vmware.vsphere.Sdk import Sdk
from k8_vmware.vsphere.VM_Process import VM_Process

class test_VM_Process(TestCase):
    def setUp(self) -> None:
        self.sdk        = Sdk()
        self.vm_name    = 'test_Photon_OS'
        self.vm         = self.sdk.find_by_name(self.vm_name)
        if self.vm is None:
            pytest.skip(f"target server did not have vm {self.vm_name}")
        else:
            if self.vm.powered_off():
                pytest.skip(f"target server exists but it not Powered On {self.vm_name}")

        self.vm_process = VM_Process(vm = self.vm)

    def test_set_vm_account_from_env(self):
        response = self.vm_process.set_vm_account_from_env(env_prefix='VSPHERE')
        print(response)

    def test_set_vm_account(self):
        self.vm_process.set_vm_account(environ.get("root"), environ.get("vmwareesxi"))

    def test_start_process_return_stdout(self):
        program_path = "/sbin/ip"
        arguments    = "a"
        self.vm_process.set_vm_account("root", "vmwareesxi")
        result       = self.vm_process.exec(program_path, arguments)
        assert 'eth0: <BROADCAST,MULTICAST,UP,LOWER_UP>' in result