import json
from pprint import pprint
from unittest import TestCase
from k8_vmware.vsphere.Sdk import Sdk

#from os import environ                     # use this to see SOAP calls made to the /sdk endpoint
#environ['show_soap_calls'] = "True"        # good to debug performance issues

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

    def test_find_by_host_name(self):
        host_name = self.sdk.vms()[0].host_name()
        #ip = self.sdk.vms()[3].dns()
        assert self.sdk.find_by_host_name(host_name).host_name() == host_name

    def test_find_by_ip(self):
        ip = self.sdk.vms()[3].ip()
        assert self.sdk.find_by_ip(ip).ip() == ip

    def test_find_by_uuid(self):
        uuid = self.sdk.vms()[0].uuid()
        assert self.sdk.find_by_uuid(uuid).uuid() == uuid


    def test_folders(self):
        folders = self.sdk.folders()
        assert str(folders) == "['vim.Folder:ha-folder-vm']"

    def test_vms(self):
        vms = self.sdk.vms()
        assert len(vms) > 0

    def test_names(self):
        names = self.sdk.vms_names()
        assert len(names) > 0
        #print(names)

    def test_service_instance(self):
        service_instance = self.sdk.service_instance()
        assert service_instance.content.about.apiVersion         == '6.7.3'
        assert service_instance.content.about.fullName           == 'VMware ESXi 6.7.0 build-16075168'
        assert service_instance.content.about.licenseProductName == 'VMware ESX Server'
        assert service_instance.content.about.osType             == 'vmnix-x86'

    def test_dump_json(self):
        obj_type = "VirtualMachine"
        moid     = "1"

        json_dump = self.sdk.json_dump(obj_type, moid)
        json_data = json.loads(json_dump)
        assert json_data['_vimid'  ] == moid
        assert json_data['_vimtype'] == "vim.VirtualMachine"