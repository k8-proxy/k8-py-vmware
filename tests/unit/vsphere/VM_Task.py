from unittest import TestCase

from k8_vmware.vsphere.VM_Task import VM_Task


class test_VM_Task(TestCase):

    def setUp(self):
        self.vm      = None
        self.vm_task = VM_Task(self.vm)

    def test__init__(self):
        assert self.vm_task.vm == self.vm