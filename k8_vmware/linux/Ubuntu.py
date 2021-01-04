from osbot_utils.decorators.methods.cache_on_self import cache_on_self

from k8_vmware.vsphere.Sdk import Sdk
from k8_vmware.vsphere.VM import VM


class Ubuntu:

    def __init__(self, vm_name):
        self.sdk     = Sdk()
        self.vm_name = vm_name

    @cache_on_self
    def vm(self) -> VM:
        return self.sdk.vm(self.vm_name)

    def exists(self) -> bool:
        return self.vm() is not None