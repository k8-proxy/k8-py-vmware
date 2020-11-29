from unittest import TestCase

from k8_vmware.vsphere.Task import Task


class test_Task(TestCase):

    def setUp(self):
        self.sdk      = None
        self.vm_task = Task(sdk=self.sdk)

    def test__init__(self):
        assert self.vm_task.sdk == self.sdk