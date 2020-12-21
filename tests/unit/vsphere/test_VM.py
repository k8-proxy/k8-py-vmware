from pprint import pprint
from unittest import TestCase

from osbot_utils.utils.Files import file_exists

from k8_vmware.helpers.Temp_VM import Temp_VM
from k8_vmware.vsphere.VM_Screenshot import VM_Screenshot


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
        assert set(self.vm.info()) == {'Notes', 'Boot_Time', 'Connection_State', 'Guest_Full_Name', 'Guest_Id', 'Host', 'Host_Name', 'IP', 'MOID', 'Max_Cpu_Usage', 'Max_Memory_Usage', 'Memory_Size_MB', 'Name', 'Num_Cpu', 'Path_Name', 'Question', 'State_State', 'UUID'} != {'Annotation', 'BootTime', 'ConnectionState', 'GuestFullName', 'GuestId', 'IP', 'MemorySizeMB', 'NumCpu', 'PathName', 'Question', 'StateState', 'UUID', 'host', 'maxCpuUsage', 'maxMemoryUsage'}

    def test_controller_ide(self):
        ide = self.vm.controller_ide()
        assert ide.key                == 200
        assert ide.deviceInfo.label   == 'IDE 0'
        assert ide.deviceInfo.summary == 'IDE 0'

    def test_send_text(self):
        self.vm.power_on()
        self.vm.send_text("a")

    def test_devices_indexed_by_label(self):
        data = self.vm.devices_indexed_by_label()
        assert list(data.keys()) == ['IDE 0', 'IDE 1', 'PS2 controller 0', 'PCI controller 0', 'SIO controller 0', 'Keyboard ', 'Pointing device', 'Video card ', 'VMCI device']

        assert data['IDE 0'].key              == 200
        assert data['IDE 0'].deviceInfo.label == 'IDE 0'

    def test_hardware(self):
        hardware = self.vm.hardware()
        assert hardware.numCPU            == 1
        assert hardware.numCoresPerSocket == 1
        assert hardware.memoryMB          == 1024
        assert len(hardware.device)       == 9


    def test_power_off(self):
        assert self.vm.powered_state()        == 'poweredOff'
        assert self.vm.power_on().info.state  == 'success'
        assert self.vm.powered_state()        == 'poweredOn'
        assert self.vm.power_off().info.state == 'success'
        assert self.vm.powered_state()        == 'poweredOff'

    def test_screenshot(self):
        self.vm.power_on()
        #self.vm.wait(1)                            # todo: when OCR serverless function is available add check to confirm text from image is the correct one
        self.vm.send_key('KEY_F2')                  # will trigger setup page
        #self.vm.wait(4)                            # todo: when OVR is available use this to detect the correct use of F2
        self.vm.send_enter()
        path_screenshot = self.vm.screenshot()
        assert file_exists(path_screenshot)

        #from osbot_utils.utils.Process import run_process
        #run_process("open", [path_screenshot])

    def test_wait(self):
        self.vm.wait(0.1)

    def test_str(self):
        assert str(self.vm) == f"[VM] {self.vm.name()}"
