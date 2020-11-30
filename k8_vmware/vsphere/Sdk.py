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



class Sdk:
    cached_service_instance = None  # use this to prevent multiple calls to the connect.SmartConnect
                                    # todo: check for side effects

    def __init__(self):
        pass

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

    def file_info(self, vm_path_name, log_directory=None, snapshot_directory=None, suspend_directory=None):
        return pyVmomi.vim.vm.FileInfo(logDirectory      = log_directory    ,
                                       snapshotDirectory = snapshot_directory,
                                       suspendDirectory  = suspend_directory ,
                                       vmPathName        = vm_path_name      )

    def find_by_host_name(self, host_name):
        search_index = self.content().searchIndex
        vm = search_index.FindByDnsName(datacenter=None, dnsName=host_name, vmSearch=True)   # note: use host_name since the documentation of this method says "The DNS name for a virtual machine is the one returned from VMware tools, hostName."
        if vm:
            return VM(vm)

    def find_by_name(self, name):
        return self.get_object_virtual_machine(name)

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

    # todo: improve this by: allowed to set how many to receive and allowing for further searches than the 'recent tasks'
    #       at the moment this can take 3 to 5 seconds to execute (since every all items are being fetched)
    def tasks_recent(self):
        content = self.content()
        task_manager = content.taskManager
        tasks = []
        for task in task_manager.recentTask:                # will make a REST call per itme
            info = task.info
            task_data = {
                "DescriptionId" : str(info.descriptionId),
                "Entity"        : str(info.entity       ).replace("'",""),
                "Key"           : str(info.key          ),
                "EventChainId"  : str(info.eventChainId ),
                "State"         : str(info.state        )
            }
            tasks.append(task_data)
            #break
        return tasks

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

    def get_objects(self, vim_type=None):
        if vim_type:
            type_names = [vim_type]
        else:
            type_names = []
        content = self.content()
        container = content.viewManager.CreateContainerView(content.rootFolder, type_names , True)
        return container.view

    def get_objects_Compute_Resources(self): return self.get_objects(pyVmomi.vim.ComputeResource)
    def get_objects_Datacenters      (self): return self.get_objects(pyVmomi.vim.Datacenter     )
    def get_objects_Datastore        (self): return self.get_objects(pyVmomi.vim.Datastore      )
    def get_objects_Hosts            (self): return self.get_objects(pyVmomi.vim.HostSystem     )
    def get_objects_Networks         (self): return self.get_objects(pyVmomi.vim.Network        )
    def get_objects_ResourcePools    (self): return self.get_objects(pyVmomi.vim.ResourcePool   )
    def get_objects_StoragePods      (self): return self.get_objects(pyVmomi.vim.StoragePod     )
    def get_objects_Virtual_Machines (self): return self.get_objects(pyVmomi.vim.VirtualMachine )

    def resource_pool(self):
        hosts =  self.datacenter().hostFolder.childEntity
        for host in hosts:
            if hasattr(host, 'resourcePool'):
                return host.resourcePool

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