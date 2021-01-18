# A list of the removed VMs will be printed
from os import environ
from dotenv import load_dotenv
from datetime import timedelta, datetime
import pytz
import sys
from k8_vmware.vsphere.Sdk import Sdk
from k8_vmware.vsphere.VM import VM


class Delete_Old_VMs:
    def __init__(self):
        load_dotenv()
        self.delete_note        = environ.get('DELETE_NOTE')
        self.dont_delete_note   = environ.get('DONT_DELETE_NOTE')
        self.esxi_expire_days   = environ.get('ESXI_EXPIRE_DAYS')
        self.sdk = Sdk()

    def __validate_days_type(self):
        if not self.esxi_expire_days or not self.esxi_expire_days.isdigit():
            print(" Expire days number must be postive integer")
            sys.exit(1)

    def vms_to_delete(self):

        removed_VMs             = []
        self.esxi_expire_days   = int(self.esxi_expire_days)
        vms                     = self.sdk.get_objects_Virtual_Machines()
        now                     = datetime.now(pytz.utc)
        for vm in vms:
            vm_info     = VM(vm)
            summary     = vm_info.summary()
            notes       = summary.config.annotation
            create_date = vm.config.createDate

            if create_date < datetime(2000, 1, 1, tzinfo=pytz.utc):
                continue

            if (self.delete_note and self.delete_note.lower() == notes.lower()) or \
                    (create_date < (now - timedelta(days=self.esxi_expire_days)) and (
                            not self.dont_delete_note or self.dont_delete_note.lower() not in notes.lower())):
                removed_VMs.append(vm_info)

        return removed_VMs

    def remove_vms(self, removed_VMs):
        removed_VMs_names = []
        for vm in removed_VMs:
            vm.task().delete()
            removed_VMs_names.append(vm.info()["Name"])
        return removed_VMs_names

    def run(self):
        self.__validate_days_type()
        removed_VMs         = self.vms_to_delete()
        removed_VMs_names   = self.remove_vms(removed_VMs)
        if removed_VMs_names:
            print("Removed VMs: ")
            print("=============")
            print("\n".join(removed_VMs_names))
        else:
            print("No VM was removed!")


def main():
    auto_delete_esxi = Delete_Old_VMs()
    auto_delete_esxi.run()


if __name__ == '__main__':
    main()
