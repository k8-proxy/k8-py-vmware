from pprint import pprint
from unittest import TestCase

from k8_vmware.vsphere.Sdk import Sdk


class test_VM(TestCase):

    def test_info(self):
        vm = Sdk().vms()[0]
        assert set(vm.info()) == {'Annotation', 'BootTime', 'ConnectionState', 'GuestFullName', 'GuestId', 'Host', 'HostName', 'IP', 'MOID', 'MaxCpuUsage', 'MaxMemoryUsage', 'MemorySizeMB', 'Name', 'NumCpu', 'PathName', 'Question', 'StateState', 'UUID'} != {'Annotation', 'BootTime', 'ConnectionState', 'GuestFullName', 'GuestId', 'IP', 'MemorySizeMB', 'NumCpu', 'PathName', 'Question', 'StateState', 'UUID', 'host', 'maxCpuUsage', 'maxMemoryUsage'}

