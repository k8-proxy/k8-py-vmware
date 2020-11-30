from unittest import TestCase

import pytest

from k8_vmware.vsphere.Sdk import Sdk
from k8_vmware.vsphere.VM_Process import VM_Process


class test_VM_Process(TestCase):
    def setUp(self) -> None:
        self.sdk        = Sdk()
        self.vm_name    = 'dinis-test-via-ovf'
        self.vm         = self.sdk.find_by_name(self.vm_name)
        if self.vm is None:
            pytest.skip(f"target server did not have vm {self.vm_name}")
        else:
            if self.vm.powered_off():
                pytest.skip(f"target server exists but it not Powered On {self.vm_name}")

        self.vm_process = VM_Process(vm = self.vm)



    def test_start_process_return_stdout(self):
        program_path = "/bin/ip"
        arguments    = "a"
        result       = self.vm_process.start_process_return_stdout(program_path, arguments)

        assert 'eth0: <BROADCAST,MULTICAST,UP,LOWER_UP>' in result

    def test_ls(self):
        assert "bin" in self.vm_process.ls('/')

