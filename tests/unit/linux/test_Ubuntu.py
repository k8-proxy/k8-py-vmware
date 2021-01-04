from pprint import pprint
from unittest import TestCase

import pyVmomi
from pytest import skip

from k8_vmware.helpers.View_Soap_Calls import View_Soap_Calls
from k8_vmware.linux.Ubuntu import Ubuntu


class test_Ubuntu(TestCase):

    def setUp(self) -> None:
        self.vm_name = "file-drop"              # todo: once we have the ability to create new VMs programatically use temp ones here
        self.ubuntu  = Ubuntu(self.vm_name)
        if self.ubuntu.vm() is None:
            skip("VM didn't exist in server")

    def test__init__(self):
        assert self.ubuntu.vm_name == self.vm_name

    def test_vm(self):
        with View_Soap_Calls():
            assert self.ubuntu.vm().name() == self.vm_name

    # todo: refactor into VM code
    def create_filter_spec(self, pc, vms, prop):
        objSpecs = []
        for vm in vms:
            objSpec = pyVmomi.vmodl.query.PropertyCollector.ObjectSpec(obj=vm)
            objSpecs.append(objSpec)
        filterSpec = pyVmomi.vmodl.query.PropertyCollector.FilterSpec()
        filterSpec.objectSet = objSpecs
        propSet = pyVmomi.vmodl.query.PropertyCollector.PropertySpec(all=False)
        propSet.type = pyVmomi.vim.VirtualMachine
        if prop:
            propSet.pathSet = [prop]
        else:
            propSet.pathSet = []
        filterSpec.propSet = [propSet]
        return filterSpec

    def test_query(self):
        sdk = self.ubuntu.sdk
        vm_name = 'fire-drop'
        args = vm_name
        result = sdk.get_object(pyVmomi.vim.VirtualMachine, args)
        pprint(result)

        args = "alarm"
        args = "parent"
        args = "config"
        args = "configStatus"
        #args = "tag"
        with View_Soap_Calls(show_calls=True, show_xml=False):
            vms = sdk.get_objects_Virtual_Machines()

            pc = sdk.service_instance().content.propertyCollector
            filter_spec = self.create_filter_spec(pc, vms, args)
            options = pyVmomi.vmodl.query.PropertyCollector.RetrieveOptions()
            result = pc.RetrievePropertiesEx([filter_spec], options)
            #pprint(result)
            #vms = filter_results(result, args.value)
            #print("VMs with %s = %s" % (args.property, args.value))
            #for vm in vms:
            #    print(vm.name)


        return




        print()

        print(self.ubuntu.sdk.vm('fire-drop'))

        print(self.ubuntu.sdk.get_object_virtual_machine(self.vm_name))
        print(self.ubuntu.vm())

        pprint(self.ubuntu.sdk.vms_names())