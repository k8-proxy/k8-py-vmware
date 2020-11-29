from osbot_utils.utils.Misc import random_string

from k8_vmware.vsphere.Sdk import Sdk


class Test_VM:

    def __init__(self):
        self.sdk       = Sdk()
        self.vm_name   = f"unit_tests__temp_vm_{random_string()}"
        self.datastore = "datastore1"
        self.guest_id  = 'ubuntu64Guest'
        self.vm        = None

    def create(self):
        self.vm = self.sdk.vm_create(self.datastore, self.vm_name, self.guest_id)
        return self.vm

    def delete(self):
        return self.sdk.vm_delete__by_name(self.vm_name)

