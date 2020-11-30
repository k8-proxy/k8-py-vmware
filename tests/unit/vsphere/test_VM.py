from pprint import pprint
from unittest import TestCase

from k8_vmware.helpers.Temp_VM import Temp_VM


class test_VM(TestCase):
    vm_name = "tests__unit__vsphere__test_VM"
    temp_vm = None

    @classmethod
    def setUpClass(cls) -> None:
        test_VM.temp_vm = Temp_VM(vm_name=test_VM.vm_name)
        test_VM.temp_vm.create()

    @classmethod
    def tearDownClass(cls) -> None:
        test_VM.temp_vm.delete()

    def setUp(self) -> None:
        self.vm = test_VM.temp_vm.vm

    def test_info(self):
        assert set(self.vm.info()) == {'Annotation', 'BootTime', 'ConnectionState', 'GuestFullName', 'GuestId', 'Host', 'HostName', 'IP', 'MOID', 'MaxCpuUsage', 'MaxMemoryUsage', 'MemorySizeMB', 'Name', 'NumCpu', 'PathName', 'Question', 'StateState', 'UUID'} != {'Annotation', 'BootTime', 'ConnectionState', 'GuestFullName', 'GuestId', 'IP', 'MemorySizeMB', 'NumCpu', 'PathName', 'Question', 'StateState', 'UUID', 'host', 'maxCpuUsage', 'maxMemoryUsage'}
