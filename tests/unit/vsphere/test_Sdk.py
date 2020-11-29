import json
from pprint import pprint
from unittest import TestCase

from k8_vmware.helpers.TestCase_VM import TestCase_VM
from k8_vmware.vsphere.Sdk import Sdk

#from os import environ                     # use this to see SOAP calls made to the /sdk endpoint
#environ['show_soap_calls'] = "True"        # good to debug performance issues
from pyVmomi import pyVmomi

class test_Sdk(TestCase_VM):
    vm_name = f"tests__unit__" + __name__

    def setUp(self):
        self.sdk = Sdk()

    def test_about(self):
        content = self.sdk.about()
        assert content.vendor                == "VMware, Inc."
        assert content.version               == "6.7.0"
        assert content.licenseProductName    == "VMware ESX Server"
        assert content.licenseProductName    == "VMware ESX Server"
        assert content.licenseProductVersion == "6.0"

    # def test_find_iso(self):
    #     vm = self.sdk.find_by_host_name('haproxy-icap')
    #     #pprint(vm.info())
    #     #print(self.sdk.json_dump("VirtualMachine","42"))
    #     #vim.vm.device.VirtualCdrom
    #     print(vm.config().hardware)

    def test_find_by_host_name(self):
        for vm in self.sdk.vms():
            host_name = vm.host_name()
            if host_name:
                assert self.sdk.find_by_host_name(host_name).host_name() == host_name
                return
        print("Warning test ESX server had no VMs with host_names (dnsNames) setup")

    def test_find_by_ip(self):
        for vm in self.sdk.vms():
            ip = vm.ip()
            if ip:
                assert self.sdk.find_by_ip(ip).ip() == ip
                return
        print("Warning test ESX server had no VMs with IPs")

    def test_find_by_uuid(self):
        uuid = self.vm.uuid()
        assert self.sdk.find_by_uuid(uuid).uuid() == uuid

    def test_get_object(self):
        name = self.vm.name()
        vm   = self.sdk.get_object(pyVmomi.vim.VirtualMachine,name)
        assert vm.name == name

    def test_get_object_virtual_machine(self):
        name = self.vm.name()
        vm   = self.sdk.get_object_virtual_machine(name)
        assert vm.name() == name

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
        assert service_instance.content.about.licenseProductName == 'VMware ESX Server'
        assert service_instance.content.about.osType             == 'vmnix-x86'

    def test_dump_json(self):

        obj_type = "VirtualMachine"
        moid     = self.vm.moid()

        json_dump = self.sdk.json_dump(obj_type, moid)
        json_data = json.loads(json_dump)
        assert json_data['_vimid'  ] == moid
        assert json_data['_vimtype'] == "vim.VirtualMachine"