from k8_vmware.vsphere.Sdk import Sdk


class Test_VMs:

    def __init__(self):
        self.sdk          = Sdk()
        self.test_vm_name = 'unit_tests_vm'

    def create_test_vm(self):
        self.sdk.vm_create()
        pass

    def delete_test_vm(self):
        pass
