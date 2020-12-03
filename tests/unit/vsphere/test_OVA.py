from pprint import pprint
from unittest import TestCase

import pyVmomi
import pytest
from osbot_utils.utils.Misc import wait

from k8_vmware.vsphere.Datastore import Datastore
from k8_vmware.vsphere.Datastore_File import Datastore_File
from k8_vmware.vsphere.OVA import OVA
from k8_vmware.vsphere.Task import Task
from k8_vmware.vsphere.VM_Process import VM_Process
from k8_vmware.vsphere.VM_Screenshot import VM_Screenshot



class test_OVA(TestCase):
    def setUp(self) -> None:
        self.ova = OVA()
        self.vm_name = 'photon'
        self.vm = self.ova.sdk.vm(self.vm_name)

        if self.vm is None:
            pytest.skip(f"target server did not have vm {self.vm_name}")

    def test__init__(self):
        assert self.ova.sdk is not None

    def test_change_password(self):  # todo: move to vm_utils calls

        photon_username         = 'root'
        photon_default_password = 'changeme'
        photon_new_password     = '{new pwd}}'

        with VM_Screenshot(self.vm) as vm:
            # note: need to wait a big before commands to allow the UI to catch up
            (
                vm.send_text(photon_username).send_enter()
                  .send_text(photon_default_password).send_enter().wait(0.2)       # send password  (starts password reset workflow)
                  .send_text(photon_default_password).send_enter().wait(0.2)       # re-enter password
                  .send_text(photon_new_password    ).send_enter().wait(0.2)       # enter new password
                  .send_text(photon_new_password    ).send_enter().wait(0.2)       # confirms new password
            )

    def test_check_pwd_change_worked(self):

        photon_username = 'root'
        photon_password = '{new pwd}}'
        vm_process = VM_Process(self.vm)
        vm_process.set_vm_account(photon_username, photon_password)
        pprint(vm_process.ls("/"))