# import pytest
# from unittest import TestCase
# from k8_vmware.vsphere.Sdk import Sdk
# from k8_vmware.vsphere.VM_Process import VM_Process
#
# class test_VM_Process(TestCase):
#     def setUp(self) -> None:
#         self.sdk        = Sdk()
#         self.vm_name    = 'dinis-test-via-ovf'
#         self.vm         = self.sdk.find_by_name(self.vm_name)
#         if self.vm is None:
#             pytest.skip(f"target server did not have vm {self.vm_name}")
#         else:
#             if self.vm.powered_off():
#                 pytest.skip(f"target server exists but it not Powered On {self.vm_name}")
#
#         self.vm_process = VM_Process(vm = self.vm)
#
#     def test_start_process_return_stdout(self):
#         program_path = "/bin/ip"
#         arguments    = "a"
#         result       = self.vm_process.start_process_return_stdout(program_path, arguments)
#         assert 'eth0: <BROADCAST,MULTICAST,UP,LOWER_UP>' in result

from os import environ
import os
import pytest
from unittest import TestCase

import wget

from k8_vmware.vsphere.OVA import OVA
from k8_vmware.vsphere.Sdk import Sdk
from k8_vmware.vsphere.VM_Process import VM_Process
from k8_vmware.vsphere.VM_Screenshot import VM_Screenshot


class test_VM_Process(TestCase):
    def setUp(self) -> None:
        self.ova = OVA()
        self.sdk=Sdk()
        if not os.path.exists('./test.ova'):
            url = "https://packages.vmware.com/photon/4.0/Beta/ova/photon-hw11-4.0-d98e681.ova"
            wget.download(url, './test.ova')
        ova_path = "./test.ova"
        self.ova.upload_ova(ova_path)


        self.vm = self.sdk.find_by_name("Photon OS")
        print(self.vm)
        self.vm.task().power_on()

        photon_username = 'root'
        photon_default_password = 'changeme'
        photon_new_password = 'vmwareesxi'

        with VM_Screenshot(self.vm) as vm:
            # note: need to wait a big before commands to allow the UI to catch up
            (
                vm.send_text(photon_username).send_enter()
                    .send_text(photon_default_password).send_enter().wait(
                    0.2)  # send password  (starts password reset workflow)
                    .send_text(photon_default_password).send_enter().wait(0.2)  # re-enter password
                    .send_text(photon_new_password).send_enter().wait(0.2)  # enter new password
                    .send_text(photon_new_password).send_enter().wait(0.2)  # confirms new password
            )

        self.vm_name    = 'Photon OS'
        self.vm         = self.sdk.find_by_name(self.vm_name)
        if self.vm is None:
            pytest.skip(f"target server did not have vm {self.vm_name}")
        else:
            if self.vm.powered_off():
                pytest.skip(f"target server exists but it not Powered On {self.vm_name}")

        self.vm_process = VM_Process(vm = self.vm)

    def test_set_vm_account_from_env(self):
        response = self.vm_process.set_vm_account_from_env(env_prefix='VSPHERE')
        print(response)

    def test_set_vm_account(self):
        self.vm_process.set_vm_account(environ.get("root"), environ.get("vmwareesxi"))

    def test_start_process_return_stdout(self):
        photon_new_password = 'vmwareesxi'
        program_path = "/sbin/ip"
        arguments    = "a"
        self.vm_process.set_vm_account("root", photon_new_password)
        result       = self.vm_process.exec(program_path, arguments)
        assert 'eth0: <BROADCAST,MULTICAST,UP,LOWER_UP>' in result

    def tearDown(self) -> None:
        self.vm.task().delete()
        if os.path.exists('./test.ova'):
            os.remove('./test.ova')