from unittest import TestCase

import pytest
from osbot_utils.utils.Misc import random_string
from k8_vmware.vsphere.Sdk import Sdk
from k8_vmware.vsphere.VM_Keystroke import VM_Keystroke
from k8_vmware.vsphere.VM_Screenshot import VM_Screenshot

# todo this test needs a test VM that we can login to (for example photon)
class test_VM_Keystroke(TestCase):
    vm_name = f"tests__unit__vsphere__Keystroke_{random_string()}"

    def setUp(self) -> None:
        sdk = Sdk()
        self.vm = sdk.vm('photon')                  # todo: refactor to use a VM we know will exist in the target Server
        self.vm_keystroke = VM_Keystroke(self.vm)
        if self.vm is None:
            pytest.skip(f"target server did not have vm {self.vm_name}")

    def test__init__(self):
        assert self.vm.name() == test_VM_Keystroke.vm_name

    def test_send_text(self):
        # todo: find way to confirm that key was actually sent
        #       at the momente we are using a screenshot (which is a pretty cool workflow)
        #       One solution is to use https://www.pyimagesearch.com/2017/07/10/using-tesseract-ocr-python/
        target_file       = '/tmp/vm_screenshot_2.png'
        with VM_Screenshot(self.vm, target_file=target_file):
            self.vm_keystroke.send_text('___')

    def test_send_char(self):
        #with VM_Screenshot(self.vm):
            self.vm_keystroke.send_char(chr(97))  # chr(97) is 'a'

    def test_send_key(self):

        #with VM_Screenshot(self.vm):
            key_enter = "KEY_ENTER"  # see list of supported keys at HIDCode array in VM_Keystroke class
            self.vm_keystroke.send_key(key_enter)

    def test_enter__esc(self):
        #with VM_Screenshot(self.vm):
            self.vm_keystroke.send_text("asdasd")      \
                             .enter()                  \
                             .esc()


    # util method
    def test_vms_ips(self):         # todo: move to Sdk to method called vms_ips() (returns object with data)
        sdk = Sdk()
        for vm in sdk.vms():
            print(f"{vm.name():30} {vm.powered_state():20} {vm.ip()}")