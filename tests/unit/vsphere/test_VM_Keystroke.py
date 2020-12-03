from unittest import TestCase

from osbot_utils.utils.Misc import random_string
from k8_vmware.vsphere.Sdk import Sdk
from k8_vmware.vsphere.VM_Keystroke import VM_Keystroke


class test_VM_Keystroke(TestCase):
    vm_name = f"tests__unit__vsphere__Keystroke_{random_string()}"

    def setUp(self) -> None:
        sdk = Sdk()
        self.vm = sdk.vm('photon')                  # todo: refactor to use a VM we know will exist in the target Server
        self.vm_keystroke = VM_Keystroke(self.vm)

    # def test__init__(self):
    #     assert self.vm.name() == test_VM_Keystroke.vm_name

    def test_send_text(self):
        # todo: find way to confirm that key was actually sent
        #       at the momente we are using a screenshot (which is a pretty cool workflow)
        #with VM_Screenshot(self.vm):
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

