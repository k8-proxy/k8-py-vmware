from unittest import TestCase

from k8_vmware.vsphere.Sdk import Sdk
from k8_vmware.vsphere.Task import Task


class test_Task(TestCase):

    def setUp(self):
        self.vm_task = Task()

    def test__init__(self):
        assert type(self.vm_task.sdk) is Sdk