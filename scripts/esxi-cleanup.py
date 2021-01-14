# This script deletes VMs that it's age exceeds the number of expire days defined in scripts/script.env file
# Except for the VMs with note that include (dont_rm_note) variable defined in scripts/script.env file
# Also will delete any VM with note that include (rm_note) variable defined in scripts/script.env file
# A list of the removed VMs will be printed
from os import environ
from dotenv import load_dotenv
from datetime import timedelta, datetime

from pathlib import Path, PurePath
import pytz
import sys

from k8_vmware.vsphere.Sdk import Sdk
from k8_vmware.vsphere.VM import VM

class AutoDeleteEsxiJob:
	def __init__(self,rm_note,dont_rm_note,expire_days_no):
		self.rm_note=rm_note
		self.dont_rm_note=dont_rm_note
		self.expire_days_no=expire_days_no

	def auto_delete(self):

		if not self.expire_days_no.isdigit():
		    print(" Expire days number must be postive integer")
		    sys.exit(1)

		self.expire_days_no=int(self.expire_days_no)
		sdk = Sdk()
		vms_o = sdk.get_objects_Virtual_Machines()
		removed_VMs = []
		now = datetime.now(pytz.utc)
		for vm_o in vms_o:
		    vm = VM(vm_o)
		    summary = vm.summary()
		    info = vm.info()
		    state=summary.runtime.powerState
		    notes  = summary.config.annotation
		    create_date=vm_o.config.createDate

		    if create_date < datetime(2000,1,1, tzinfo=pytz.utc):
		        continue

		    if (self.rm_note and self.rm_note.lower() in notes.lower()) or \
		    (create_date < (now - timedelta(days=self.expire_days_no)) and (not self.dont_rm_note or self.dont_rm_note.lower() not in notes.lower())):
		    	if state == 'poweredOn':
		    		vm.task().power_off()
		    	vm.task().delete()
		    	removed_VMs.append(info["Name"])

		if removed_VMs:
		    print("Removed VMs: ")
		    print("=============")
		    print("\n".join(removed_VMs))
		else:
		    print("No VM was removed!")

def main():
	env_path= PurePath(__file__).parent / 'script.env'
	load_dotenv(dotenv_path=env_path)
	load_dotenv()
	rm_note=environ.get('rm_note')
	dont_rm_note=environ.get('dont_rm_note')
	expire_days_no=environ.get('expire_days_no','')
	auto_delete_esxi=AutoDeleteEsxiJob(rm_note,dont_rm_note,expire_days_no)
	auto_delete_esxi.auto_delete()



if __name__ == '__main__':
	main()

