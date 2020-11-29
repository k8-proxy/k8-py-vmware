import atexit
import json
import  ssl

import  pyVmomi
import  urllib3
import  warnings
from    pyVim import connect
from    pyVim.connect import Disconnect
from    pyVmomi       import VmomiSupport

from k8_vmware.Config import Config
from k8_vmware.vsphere.VM import VM

# see https://code.vmware.com/apis/968 for API details
from k8_vmware.vsphere.VM_Task import VM_Task


class Sdk:
    cached_service_instance = None  # use this to prevent multiple calls to the connect.SmartConnect
                                    # todo: check for side effects

    def __init__(self):
        self._service_instance = None

    # helper methods
    def unverified_ssl_context(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        warnings.simplefilter("ignore", ResourceWarning)
        sslContext = ssl._create_unverified_context()
        return sslContext

    def server_details(self):
        return Config().vsphere_server_details()

    # Sdk methods

    def about(self):
        return self.content().about

    def content(self):
        return self.service_instance().RetrieveContent()

    def find_by_host_name(self, host_name):
        search_index = self.content().searchIndex
        vm = search_index.FindByDnsName(datacenter=None, dnsName=host_name, vmSearch=True)   # note: use host_name since the documentation of this method says "The DNS name for a virtual machine is the one returned from VMware tools, hostName."
        if vm:
            return VM(vm)

    # todo: refactor to use method that doesn't require iterating through all vms to find one that matches the name
    def find_by_name(self, name):
        for vm in self.vms():
            if vm.name() == name:
                return vm

    def find_by_uuid(self, uuid):
        search_index = self.content().searchIndex
        vm = search_index.FindByUuid(datacenter=None, uuid=uuid, vmSearch=True)
        if vm:
            return VM(vm)

    def find_by_ip(self, ip_address):
        search_index = self.content().searchIndex
        vm = search_index.FindByIp(datacenter=None, ip=ip_address, vmSearch=True)
        if vm:
            return VM(vm)

    def json_dump(self, obj_type, moid):
        si_stub  = self.service_instance()._stub
        template = VmomiSupport.templateOf(obj_type)
        encoder  = VmomiSupport.VmomiJSONEncoder
        raw_obj  = template(moid, si_stub)
        return json.dumps(raw_obj, cls=encoder, sort_keys=True, indent=4)

    def service_instance(self):
        server      = self.server_details()
        host        = server['host']
        user        = server['username']
        pwd         = server['password']
        ssl_context = self.unverified_ssl_context()
        try:
            if (Sdk.cached_service_instance is None):
                Sdk.cached_service_instance = connect.SmartConnect(host=host, user=user, pwd=pwd, sslContext=ssl_context)
                atexit.register(Disconnect, self.service_instance)
        except Exception as exception:
            if(exception._wsdlName == 'InvalidLogin'):
                raise Exception(f"[vsphere][sdk] login failed for user {user}")
            else:
                raise exception

        return Sdk.cached_service_instance

    def datacenter(self):
        for child in self.content().rootFolder.childEntity:
            if child._wsdlName == 'Datacenter':
                return child

    def datacenter_folder(self):
        datacenter = self.datacenter()
        if hasattr(datacenter, 'vmFolder'):
            return datacenter.vmFolder

    def folders(self):
        folders = []
        for child in self.content().rootFolder.childEntity:     # todo: add better support for datacenter
            datacenter = child                                  # this code assumes that this node is an of type 'vim.Datacenter:ha-datacenter'
            if hasattr(datacenter, 'vmFolder'):                 # if it has folders addit
                folders.append(datacenter.vmFolder)             # todo: add support for nested folders (see code at https://github.com/vmware/pyvmomi/blob/master/sample/getallvms.py#L58 )
        return folders

    def get_object(self, vim_type, name):
        content = self.content()
        container = content.viewManager.CreateContainerView(content.rootFolder, [vim_type], True)
        for object in container.view:
            if object.name == name:
                return object

    def get_object_virtual_machine(self, name):
        vm = self.get_object(pyVmomi.vim.VirtualMachine, name)
        if vm:
            return VM(vm)

    def resource_pool(self):
        hosts =  self.datacenter().hostFolder.childEntity
        for host in hosts:
            if hasattr(host, 'resourcePool'):
                return host.resourcePool

    # todo refactor into VM_Create class
    def vm_create(self, datastore, vm_name, guest_id):

        service_instance = self.service_instance()
        datacenter       = self.datacenter()
        folder           = self.datacenter_folder()
        resource_pool    = self.resource_pool()

        datastore_path = '[' + datastore + '] ' + vm_name

        # bare minimum VM shell, no disks. todo: add these as special options
        vmx_file = pyVmomi.vim.vm.FileInfo(logDirectory=None,
                                           snapshotDirectory=None,
                                           suspendDirectory=None,
                                           vmPathName=datastore_path)

        config = pyVmomi.vim.vm.ConfigSpec(name=vm_name, memoryMB=128, numCPUs=1,
                                           files=vmx_file, guestId=guest_id,
                                           version='vmx-07')

        task = folder.CreateVM_Task(config=config, pool=resource_pool)
        VM_Task(self).wait_for_task(task)

        return  VM(task.info.result)        # return a vm object
        #return task


    def vm_delete(self, vm : VM):
        pass

    # name = "dinis-test-via-api"
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

    def vm_delete__by_name(self, vm_name : str):
        vm = self.find_by_name(vm_name)
        if vm:
            if vm.powered_on():
                # todo: add power off task
                pass

            task_destroy = vm.vm.Destroy_Task()
            return VM_Task(self).wait_for_task(task_destroy)


    def vms(self):
        vms = []
        for folder in self.folders():
            for vm in folder.childEntity:
                vms.append(VM(vm))
        return vms

    def vms_names(self):
        names = []
        for vm in self.vms():
            names.append(vm.name())
        return names

        # ## alternative way to get the names (via CreateContainerView)
        # ## this does seem to make a couple less REST calls than the current view
        # def names_v2(self):
        #     # from pyVmomi import vim, vmodl
        #     from pyVmomi import pyVmomi
        #     content = Sdk().content()
        #
        #     objView = content.viewManager.CreateContainerView(content.rootFolder,
        #                                                       [pyVmomi.vim.VirtualMachine],
        #                                                       True)
        #     vmList = objView.view
        #     for vm in vmList:
        #         print(vm.name)            # will make REST call here