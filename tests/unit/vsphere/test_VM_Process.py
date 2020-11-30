from unittest import TestCase

import pytest

from k8_vmware.vsphere.VM_Process import VM_Process


class test_VM_Process(TestCase):
    def setUp(self) -> None:
        self.vm_name    = 'dinis-test-via-ovf'
        self.vm_process = VM_Process(self.vm_name)
        if self.vm_process.find_vm() is None:
            pytest.skip(f"target server did not have vm {self.vm_name}")


    def test_start_process_return_stdout(self):
        program_path = "/bin/ip"
        arguments    = "a"
        result       = self.vm_process.start_process_return_stdout(program_path, arguments)

        assert 'eth0: <BROADCAST,MULTICAST,UP,LOWER_UP>' in result

    def test_ls(self):
        assert "bin" in self.vm_process.ls('/')

