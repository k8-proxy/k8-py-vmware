# This script removes all VMs that have a keyword 'delete' in the the Notes section in VMware ESXi

from k8_vmware.vsphere.Sdk import Sdk
from k8_vmware.vsphere.VM import VM

sdk = Sdk()
vms_o = sdk.get_objects_Virtual_Machines()
removed_VMs = []
for vm_o in vms_o:
    vm = VM(vm_o)
    summary = vm.summary()
    info = vm.info()
    notes  = summary.config.annotation               
    if 'delete'.lower() in notes.lower():
        removed_VMs.append(info["Name"])
        vm.task().delete()

print("Removed VMs: ")
print("=============")
print("\n".join(removed_VMs))