import json
from pprint import pprint
from unittest import TestCase
from k8_vmware.vsphere.Sdk import Sdk

#from os import environ                     # use this to see SOAP calls made to the /sdk endpoint
#environ['show_soap_calls'] = "True"        # good to debug performance issues

from pyVmomi import vim
from pyVmomi import vmodl

def wait_for_tasks(service_instance, tasks):
    """Given the service instance si and tasks, it returns after all the
   tasks are complete
   """
    property_collector = service_instance.content.propertyCollector
    task_list = [str(task) for task in tasks]
    # Create filter
    obj_specs = [vmodl.query.PropertyCollector.ObjectSpec(obj=task)
                 for task in tasks]
    property_spec = vmodl.query.PropertyCollector.PropertySpec(type=vim.Task,
                                                               pathSet=[],
                                                               all=True)
    filter_spec = vmodl.query.PropertyCollector.FilterSpec()
    filter_spec.objectSet = obj_specs
    filter_spec.propSet = [property_spec]
    pcfilter = property_collector.CreateFilter(filter_spec, True)
    try:
        version, state = None, None
        # Loop looking for updates till the state moves to a completed state.
        while len(task_list):
            update = property_collector.WaitForUpdates(version)
            for filter_set in update.filterSet:
                for obj_set in filter_set.objectSet:
                    task = obj_set.obj
                    for change in obj_set.changeSet:
                        if change.name == 'info':
                            state = change.val.state
                        elif change.name == 'info.state':
                            state = change.val
                        else:
                            continue

                        if not str(task) in task_list:
                            continue

                        if state == vim.TaskInfo.State.success:
                            # Remove task from taskList
                            task_list.remove(str(task))
                        elif state == vim.TaskInfo.State.error:
                            raise task.info.error
            # Move to next version
            version = update.version
    finally:
        if pcfilter:
            pcfilter.Destroy()

class test_Sdk(TestCase):

    def setUp(self):
        self.sdk = Sdk()

    def test_about(self):
        content = self.sdk.about()
        assert content.fullName              == "VMware ESXi 6.7.0 build-16075168"
        assert content.vendor                == "VMware, Inc."
        assert content.version               == "6.7.0"
        assert content.licenseProductName    == "VMware ESX Server"
        assert content.licenseProductName    == "VMware ESX Server"
        assert content.licenseProductVersion == "6.0"


    # def test_find_iso(self):
    #     vm = self.sdk.find_by_host_name('haproxy-icap')
    #     #pprint(vm.info())
    #     #print(self.sdk.json_dump("VirtualMachine","42"))
    #     #vim.vm.device.VirtualCdrom
    #     print(vm.config().hardware)

    # def test_delete_vm(self):
    #
    #     name = "dinis-test-via-api"
    #     vm = self.sdk.find_by_name(name)
    #     pprint(vm.info())
    #
    #     si = self.sdk.service_instance()
    #     # task_power_off = vm.vm.PowerOffVM_Task()
    #     # wait_for_tasks(si, [task_power_off])
    #
    #     task_destroy = vm.vm.Destroy_Task()
    #     wait_for_tasks(si, [task_destroy])
    #
    #     vm = self.sdk.find_by_name(name)
    #     pprint(vm.info())
    #     #pprint(self.sdk.vms()[16].info())

    # def test_create_vm(self):
    #
    #
    #
    #     def get_obj(content, vimtype, name):
    #         obj = None
    #         container = content.viewManager.CreateContainerView(
    #             content.rootFolder, vimtype, True)
    #         for c in container.view:
    #             if c.name == name:
    #                 obj = c
    #                 break
    #         return obj
    #
    #     from pyVmomi import vim, vmodl
    #     #from add_nic_to_vm import add_nic, get_obj
    #
    #
    #     #pprint(self.sdk.vms()[0].info())
    #     #return
    #     """Creates a dummy VirtualMachine with 1 vCpu, 128MB of RAM.
    #         :param name: String Name for the VirtualMachine
    #         :param service_instance: ServiceInstance connection
    #         :param vm_folder: Folder to place the VirtualMachine in
    #         :param resource_pool: ResourcePool to place the VirtualMachine in
    #         :param datastore: DataStrore to place the VirtualMachine on
    #         """
    #     content = service_instance = self.sdk.content()
    #
    #     #content = service_instance.RetrieveContent()
    #     datacenter = ""
    #     folder = ""
    #     resource_pool = ""
    #
    #     # print()
    #     # vm_datacenter = get_obj(content, [vim.Datacenter], "")
    #     # vm_folder = get_obj(content, [vim.Folder], folder)
    #     # vm_resource_pool = get_obj(content, [vim.ResourcePool], resource_pool)
    #     # print(vm_datacenter, vm_folder, vm_resource_pool)
    #     #
    #     # vm_folder = self.sdk.datacenter_folder()
    #     # vm_datacenter = self.sdk.datacenter()
    #     #
    #     # print(self.sdk.datacenter())
    #     # print(self.sdk.datacenter_folder())
    #
    #     service_instance = self.sdk.service_instance()
    #     vm_datacenter    = self.sdk.datacenter()
    #     vm_folder        = self.sdk.datacenter_folder()
    #     vm_resource_pool = self.sdk.resource_pool()
    #
    #
    #     datastore = "datastore1"
    #     vm_name = "dinis-test-via-api"
    #     datastore_path = '[' + datastore + '] ' + vm_name
    #
    #     # bare minimum VM shell, no disks. Feel free to edit
    #     vmx_file = vim.vm.FileInfo(logDirectory=None,
    #                                snapshotDirectory=None,
    #                                suspendDirectory=None,
    #                                vmPathName=datastore_path)
    #
    #     config = vim.vm.ConfigSpec(name=vm_name, memoryMB=128, numCPUs=1,
    #                                files=vmx_file, guestId='ubuntu64Guest',
    #                                version='vmx-07')
    #
    #     print("Creating VM {}...".format(vm_name))
    #     task = vm_folder.CreateVM_Task(config=config, pool=vm_resource_pool)
    #     wait_for_tasks(service_instance, [task])

    def test_find_by_host_name(self):
        host_name = self.sdk.vms()[0].host_name()
        #ip = self.sdk.vms()[3].dns()
        assert self.sdk.find_by_host_name(host_name).host_name() == host_name

        pprint(self.sdk.find_by_host_name('minio-server').info())

    def test_find_by_ip(self):
        ip = self.sdk.vms()[3].ip()
        assert self.sdk.find_by_ip(ip).ip() == ip

    def test_find_by_uuid(self):
        uuid = self.sdk.vms()[0].uuid()
        assert self.sdk.find_by_uuid(uuid).uuid() == uuid

    def test_get_object(self):
        name = self.sdk.vms()[0].name()
        vm   = self.sdk.get_object(vim.VirtualMachine,name)
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
        assert service_instance.content.about.fullName           == 'VMware ESXi 6.7.0 build-16075168'
        assert service_instance.content.about.licenseProductName == 'VMware ESX Server'
        assert service_instance.content.about.osType             == 'vmnix-x86'

    def test_dump_json(self):
        obj_type = "VirtualMachine"
        moid     = "1"

        json_dump = self.sdk.json_dump(obj_type, moid)
        json_data = json.loads(json_dump)
        assert json_data['_vimid'  ] == moid
        assert json_data['_vimtype'] == "vim.VirtualMachine"