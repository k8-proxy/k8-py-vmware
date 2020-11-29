import json
from pprint import pprint
from unittest import TestCase
from k8_vmware.vsphere.Sdk import Sdk

#from os import environ                     # use this to see SOAP calls made to the /sdk endpoint
#environ['show_soap_calls'] = "True"        # good to debug performance issues
from pyVmomi import pyVmomi
#from pyVmomi import vim
#from pyVmomi import vmodl

# def wait_for_tasks(service_instance, tasks):
#     """Given the service instance si and tasks, it returns after all the
#    tasks are complete
#    """
#     property_collector = service_instance.content.propertyCollector
#     task_list = [str(task) for task in tasks]
#     # Create filter
#     obj_specs = [pyVmomi.vmodl.query.PropertyCollector.ObjectSpec(obj=task)
#                  for task in tasks]
#     property_spec = pyVmomi.vmodl.query.PropertyCollector.PropertySpec(type=pyVmomi.vim.Task,
#                                                                        pathSet=[],
#                                                                        all=True)
#     filter_spec = pyVmomi.vmodl.query.PropertyCollector.FilterSpec()
#     filter_spec.objectSet = obj_specs
#     filter_spec.propSet = [property_spec]
#     pcfilter = property_collector.CreateFilter(filter_spec, True)
#     try:
#         version, state = None, None
#         # Loop looking for updates till the state moves to a completed state.
#         while len(task_list):
#             update = property_collector.WaitForUpdates(version)
#             for filter_set in update.filterSet:
#                 for obj_set in filter_set.objectSet:
#                     task = obj_set.obj
#                     for change in obj_set.changeSet:
#                         if change.name == 'info':
#                             state = change.val.state
#                         elif change.name == 'info.state':
#                             state = change.val
#                         else:
#                             continue
#
#                         if not str(task) in task_list:
#                             continue
#
#                         if state == pyVmomi.vim.TaskInfo.State.success:
#                             # Remove task from taskList
#                             task_list.remove(str(task))
#                         elif state == pyVmomi.vim.TaskInfo.State.error:
#                             raise task.info.error
#             # Move to next version
#             version = update.version
#     finally:
#         if pcfilter:
#             pcfilter.Destroy()
from k8_vmware.vsphere.VM import VM


class test_Sdk(TestCase):

    def setUp(self):
        self.sdk = Sdk()

    def test_about(self):
        content = self.sdk.about()
        assert content.vendor                == "VMware, Inc."
        assert content.version               == "6.7.0"
        assert content.licenseProductName    == "VMware ESX Server"
        assert content.licenseProductName    == "VMware ESX Server"
        assert content.licenseProductVersion == "6.0"

    def test_vm_create__delete_by_name(self):
        print()
        datastore       = "datastore1"
        vm_name         = "unittest-test_vm_create__delete_by_name"
        guest_id        = 'ubuntu64Guest'
        vm_created_info = self.sdk.vm_create(datastore, vm_name, guest_id).info()
        task_delete     = self.sdk.vm_delete__by_name(vm_name)

        assert vm_created_info['Name'] == vm_name
        assert task_delete.info.state == "success"

    # def test_find_iso(self):
    #     vm = self.sdk.find_by_host_name('haproxy-icap')
    #     #pprint(vm.info())
    #     #print(self.sdk.json_dump("VirtualMachine","42"))
    #     #vim.vm.device.VirtualCdrom
    #     print(vm.config().hardware)

    def test_find_by_host_name(self):
        for vm in self.sdk.vms():
            host_name = vm.host_name()
            if host_name:
                assert self.sdk.find_by_host_name(host_name).host_name() == host_name
                return
        print("Warning test ESX server had no VMs with host_names (dnsNames) setup")

    def test_find_by_ip(self):
        for vm in self.sdk.vms():
            ip = vm.ip()
            if ip:
                assert self.sdk.find_by_ip(ip).ip() == ip
                return
        print("Warning test ESX server had no VMs with IPs")

    def test_find_by_uuid(self):
        uuid = self.sdk.vms()[0].uuid()
        assert self.sdk.find_by_uuid(uuid).uuid() == uuid

    def test_get_object(self):
        name = self.sdk.vms()[0].name()
        vm   = self.sdk.get_object(pyVmomi.vim.VirtualMachine,name)
        assert vm.name == name

    def test_get_object_virtual_machine(self):
        print('===')
        name = self.sdk.vms()[0].name()
        print('===')
        vm   = self.sdk.get_object_virtual_machine(name)
        print('===')
        assert vm.name() == name

    def test_folders(self):
        folders = self.sdk.folders()
        assert str(folders) == "['vim.Folder:ha-folder-vm']"

    def test_vms(self):
        vms = self.sdk.vms()
        assert len(vms) > 0

    def test_names(self):
        names = self.sdk.vms_names()
        assert len(names) > 0
        #print(names)

    def test_service_instance(self):
        service_instance = self.sdk.service_instance()
        assert service_instance.content.about.apiVersion         == '6.7.3'
        assert service_instance.content.about.licenseProductName == 'VMware ESX Server'
        assert service_instance.content.about.osType             == 'vmnix-x86'

    def test_dump_json(self):

        obj_type = "VirtualMachine"
        moid     = self.sdk.vms()[0].moid()

        json_dump = self.sdk.json_dump(obj_type, moid)
        json_data = json.loads(json_dump)
        assert json_data['_vimid'  ] == moid
        assert json_data['_vimtype'] == "vim.VirtualMachine"