from osbot_utils.utils.Misc import random_string

from k8_vmware.vsphere.Sdk import Sdk
from k8_vmware.vsphere.VM import VM


class Temp_VM:

    def __init__(self, vm_name=None):
        self.sdk       = Sdk()
        self.vm_name   = vm_name or f"unit_tests__temp_vm_{random_string()}"
        self.datastore = "datastore1"
        self.guest_id  = 'ubuntu64Guest'
        self.vm        = None

    def __enter__(self):
        return self.create()

    def __exit__(self, type, value, traceback):
        self.delete()

    def create(self):
        self.vm = self.sdk.vm_create(self.datastore, self.vm_name, self.guest_id)
        return self.vm

    def delete(self):
        return self.sdk.vm_delete(self.vm)

