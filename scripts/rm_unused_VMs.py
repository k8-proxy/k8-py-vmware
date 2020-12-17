# This script removes all VMs that have a keyword in the the Notes section in VMware ESXi
# The keyword should be defined as an environment variable "rm_keyword"
# A list of the removed VMs will be printed

from os import environ
from dotenv import load_dotenv
from k8_vmware.vsphere.Sdk import Sdk
from k8_vmware.vsphere.VM import VM

rm_keyword = environ.get('rm_keyword')
sdk = Sdk()
vms_o = sdk.get_objects_Virtual_Machines()
removed_VMs = []
for vm_o in vms_o:
    vm = VM(vm_o)
    summary = vm.summary()
    info = vm.info()
    notes  = summary.config.annotation               
    if rm_keyword.lower() in notes.lower():
        removed_VMs.append(info["Name"])
        vm.task().delete()

if removed_VMs:
    print("Removed VMs: ")
    print("=============")
    print("\n".join(removed_VMs))
else:
    print("No VM was removed!")