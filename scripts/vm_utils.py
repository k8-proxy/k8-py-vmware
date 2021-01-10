from os import environ
from dotenv import load_dotenv
from k8_vmware.vsphere.Sdk import Sdk
from k8_vmware.vsphere.VM import VM

load_dotenv()


class VMUtils:
    """
    Contains method to start or stop VM based on input conditions.
    Required environment variables:
    VSPHERE_HOST=
    VSPHERE_USERNAME=
    VSPHERE_PASSWORD=
    mode_tag=start|shutdown
    start_shut_tag=
    not_shutdown_tag=
    """

    def __init__(self):
        self.mode_tag = environ.get("mode_tag", None)
        self.start_shut_tag = environ.get("start_shut_tag", None)
        self.not_shutdown_tag = environ.get("not_shutdown_tag", None)

        self.sdk = Sdk()

    def _get_vms(self):
        return self.sdk.get_objects_Virtual_Machines()

    def process_vm(self, vm):
        altered = False
        summary = vm.summary()
        notes = summary.config.annotation.lower()
        # print(f"Processing VM : {vm}, Note: {notes}")
        if notes:
            if self.not_shutdown_tag:
                if self.not_shutdown_tag.lower() in notes:
                    return False

            if self.start_shut_tag.lower() in notes:
                if self.mode_tag in ["start", "shutdown"]:
                    altered = vm.info()["Name"]
                    if self.mode_tag == "start":
                        print("starting..", altered)
                        try:
                            vm.power_on()
                        except Exception as ex:
                            print(str(ex))
                    else:
                        print("shutting down..", altered)
                        try:
                            vm.power_off()
                        except Exception as ex:
                            print(str(ex))

        return altered

    def process(self):
        if not self.mode_tag or not self.start_shut_tag:
            print("`mode_tag` or `start_shut_tag` is not defined on env vars")
            return

        if self.mode_tag == "" or self.start_shut_tag == "":
            print("`mode_tag` or `start_shut_tag` should not be blank")
            return

        altered_vms = []
        vms_o = self._get_vms()
        print(f"total vms : {len(vms_o)}")

        for vm_o in vms_o:
            vm = VM(vm_o)
            altered = self.process_vm(vm)
            if altered:
                altered_vms.append(altered)

        if altered_vms:
            print("Altered VMs: ")
            print("=============")
            print("\n".join(altered_vms))
        else:
            print("No VM was Altered !")


VMUtils().process()
