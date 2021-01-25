from os import environ
from dotenv import load_dotenv
import datetime
import time

from k8_vmware.vsphere.Sdk import Sdk
from .utils import Utils


class Esxi_Power:
    """
    Contains method to start or stop VM based on input conditions.
    """

    def __init__(self):
        load_dotenv()
        self.mode_tag = environ.get("mode_tag", None)
        self.start_shut_tag = environ.get("start_shut_tag", None)
        self.not_shutdown_tag = environ.get("not_shutdown_tag", None)
        self.auto = int(environ.get("auto", 0))

        self.sdk = Sdk()
        self.dt_format = "%Y-%m-%d %I:%M%p"
        self.action_maps = {"start": "power_on", "shutdown": "power_off"}

    def _get_vms(self):
        return self.sdk.vms()

    def get_targets(self):
        vms = self._get_vms()
        print(f"total vms : {len(vms)}")
        return vms

    def do_action(self, action, vm):
        vm_name = vm.name()
        if action not in self.action_maps.values():
            print(f"invalid action : {action}")
            return
        print(f"{vm_name} : {action}")
        try:
            f = getattr(vm, self.action_maps.get(action))
            # f()
        except Exception as ex:
            raise Exception(str(ex))

        return vm_name

    def process_vm(self, vm):
        altered = False
        summary = vm.summary()
        notes = summary.config.annotation.lower()
        # print(f"Processing VM : {vm}, Note: {notes}")
        if not notes:
            print("No notes present on VM")
            return False

        if self.not_shutdown_tag:
            if self.not_shutdown_tag.lower() in notes:
                return False

        tag_present = self.start_shut_tag.lower() in notes
        action_present = self.mode_tag in self.action_maps.keys()
        if tag_present and action_present:
            altered = self.do_action(self.mode_tag, vm)

        return altered

    def process(self):
        altered_vms = []
        vms = self.get_targets()
        for vm in vms:
            altered = self.process_vm(vm)
            if altered:
                altered_vms.append(altered)

        if altered_vms:
            print("Altered VMs: ")
            print("=============")
            print("\n".join(altered_vms))
        else:
            print("No VM was Altered !")

    def validate_scheduled_mode(self):
        expected_dt = None
        if self.mode_tag == "start":
            expected_dt = environ.get("scheduled_start", None)
        elif self.mode_tag == "shutdown":
            expected_dt = environ.get("scheduled_stop", None)
        if not expected_dt:
            raise Exception("`scheduled_start` or `scheduled_stop` not provided")
        return expected_dt

    def start(self):
        if not self.mode_tag or not self.start_shut_tag:
            print("`mode_tag` or `start_shut_tag` is not defined on env vars")
            return

        if self.mode_tag == "" or self.start_shut_tag == "":
            print("`mode_tag` or `start_shut_tag` should not be blank")
            return

        process = True
        if self.auto == 1:
            print("scheduled mode...")
            expected_dt = self.validate_scheduled_mode()
            expected_dt = Utils.format_expected_date(expected_dt, self.dt_format)

            # wait until time
            current_dt = None
            while expected_dt != current_dt:
                print(expected_dt, current_dt)
                time.sleep(30)
                current_dt = datetime.datetime.strftime(
                    datetime.datetime.now(), self.dt_format
                )

            if current_dt == expected_dt:
                process = True

        if process:
            self.process()


def main():
    Esxi_Power().start()


if __name__ == "__main__":
    main()
