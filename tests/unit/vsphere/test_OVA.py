import time
from unittest import TestCase
import os
import pyVmomi
import pytest
from osbot_utils.utils.Files import file_exists
from osbot_utils.utils.Misc import wait

from k8_vmware.vsphere.Datastore import Datastore
from k8_vmware.vsphere.Datastore_File import Datastore_File
from k8_vmware.vsphere.OVA import OVA, OvfHandler
from k8_vmware.vsphere.Sdk import Sdk
from k8_vmware.vsphere.Task import Task
from k8_vmware.vsphere.VM_Process import VM_Process
from k8_vmware.vsphere.VM_Screenshot import VM_Screenshot

import wget
class test_OVA(TestCase):
    def setUp(self) -> None:
        self.ova = OVA()
        #self.vm_name = 'photon'
        #self.vm = self.ova.sdk.vm(self.vm_name)

        #if self.vm is None:
        #    pytest.skip(f"target server did not have vm {self.vm_name}")

    def test__init__(self):
        assert self.ova.sdk is not None

    def test_upload_ova_file(self):
        sdk=Sdk()
        if not os.path.exists('./test.ova'):
            url = "https://packages.vmware.com/photon/4.0/Beta/ova/photon-hw11-4.0-d98e681.ova"
            wget.download(url, './test.ova')
        ova_path="./test.ova"
        self.ova.upload_ova(ova_path)
        self.vm = sdk.find_by_name("Photon OS")
        print(self.vm)
        self.vm.task().delete()

    def test_upload_ova_web(self):
        sdk=Sdk()
        url = "https://packages.vmware.com/photon/4.0/Beta/ova/photon-hw11-4.0-d98e681.ova"
        self.ova.upload_ova(url)
        self.vm = sdk.find_by_name("Photon OS")
        print(self.vm)
        self.vm.task().delete()

class test_OvfHandler(TestCase):
    def setUp(self) -> None:
        self.ova_path="./test.ova"
        self.ova_handler = OvfHandler(self.ova_path)
        self.url="https://packages.vmware.com/photon/4.0/Beta/ova/photon-hw11-4.0-d98e681.ova"

    def test_create_file_handle(self):
        response=self.ova_handler._create_file_handle(self.url)
        assert response is not None
        assert response.tell() is not None
        assert response.seekable() is True

    def test_get_descriptor(self):
        response=self.ova_handler.get_descriptor()
        assert response is not None