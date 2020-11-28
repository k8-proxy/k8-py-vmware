from unittest import TestCase

from k8_vmware.vsphere.Sdk import Sdk


class test_Sdk(TestCase):
    def setUp(self):
        self.sdk = Sdk()

    def test_service_instance(self):
        print(self.sdk.service_instance())