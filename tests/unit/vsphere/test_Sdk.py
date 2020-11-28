from unittest import TestCase

from k8_vmware.vsphere.Sdk import Sdk


class test_Sdk(TestCase):
    def setUp(self):
        self.sdk = Sdk()

    def test_about(self):
        content = self.sdk.about()
        assert content.fullName              == "VMware ESXi 6.7.0 build-16075168"
        assert content.vendor                == "VMware, Inc."
        assert content.version               == "6.7.0"
        assert content.licenseProductName    == "VMware ESX Server"
        assert content.licenseProductName    == "VMware ESX Server"
        assert content.licenseProductVersion == "6.0"

    def test_service_instance(self):
        service_instance = self.sdk.service_instance()
        assert service_instance.content.about.apiVersion         == '6.7.3'
        assert service_instance.content.about.fullName           == 'VMware ESXi 6.7.0 build-16075168'
        assert service_instance.content.about.licenseProductName == 'VMware ESX Server'
        assert service_instance.content.about.osType             == 'vmnix-x86'