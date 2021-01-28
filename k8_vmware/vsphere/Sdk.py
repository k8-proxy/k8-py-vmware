import atexit
import json
import  ssl
from subprocess import PIPE, Popen

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
        self.login_exception = None

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

    def about_name(self):
        return self.about().name

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
        vm = self.get_object_virtual_machine(name)
        if vm:
            return VM(vm)

    def find_by_uuid(self, uuid, instance_uuid=False):
        search_index = self.content().searchIndex
        if instance_uuid:
            vm = search_index.FindByUuid(datacenter=None, uuid=uuid, vmSearch=True, instanceUuid=True)
        else:
            vm = search_index.FindByUuid(datacenter=None, uuid=uuid, vmSearch=True)
        if vm:
            return VM(vm)

    def find_by_ip(self, ip_address):
        search_index = self.content().searchIndex
        vm = search_index.FindByIp(datacenter=None, ip=ip_address, vmSearch=True)
        if vm:
            return VM(vm)

    def login(self, host=None, user_id=None, password=None, force_reload=False):
        try:
            self.login_exception = None
            if (user_id and password):
                config = Config()
                config.vsphere_set_server_details(host=host, username=user_id, password=password)
                force_reload=True
            self.service_instance(force_reload=force_reload)
            return True
        except Exception as exception:
            self.login_exception = exception
            return False

    # note: give the current maturity of this API this method doesn't have a lot of uses
    # def json_dump(self, obj_type, moid):
    #     si_stub  = self.service_instance()._stub
    #     template = VmomiSupport.templateOf(obj_type)
    #     encoder  = VmomiSupport.VmomiJSONEncoder
    #     raw_obj  = template(moid, si_stub)
    #     return json.dumps(raw_obj, cls=encoder, sort_keys=True, indent=4)

    def service_instance(self, force_reload=False):
        server      = self.server_details()
        host        = server['host']
        user        = server['username']
        pwd         = server['password']
        ssl_context = self.unverified_ssl_context()             # todo: make this a option that is configurable (default should not be this insecure mode)
        try:
            if (force_reload or Sdk.cached_service_instance is None):
                Sdk.cached_service_instance = None
                Sdk.cached_service_instance = connect.SmartConnect(host=host, user=user, pwd=pwd, sslContext=ssl_context)
                atexit.register(Disconnect, self.service_instance)
        except Exception as exception:
            if(exception._wsdlName == 'InvalidLogin'):
                raise Exception(f"[vsphere][sdk] login failed for user {user} : {exception.msg}") from None
            else:
                raise exception

        return Sdk.cached_service_instance

    # todo: improve this by: allowed to set how many to receive and allowing for further searches than the 'recent tasks'
    #       at the moment this can take 3 to 5 seconds to execute (since every all items are being fetched)
#     def tasks_recent_experiment(self, entity):
#         # below worked
#         from osbot_utils.utils.Process import exec_process
#         result = exec_process("ssh", ['-t', 'root@esxi04.glasswall-icap.com', 'ls','/var/log'])
#
#         from pprint import pprint
#         pprint(result)
#
#         return
#         content = self.content()
#         task_manager = content.taskManager
#         object_type =  pyVmomi.vim.Task
#         target_objects = task_manager.recentTask
#         #properties_names = [ 'dynamicType', 'dynamicProperty', 'key', 'task','description', 'name', 'descriptionId', 'entity', 'entityName', 'locked', 'state', 'cancelled', 'cancelable', 'error', 'result', 'progress', 'reason', 'queueTime', 'startTime', 'completeTime', 'eventChainId', 'changeTag', 'parentTaskKey', 'rootTaskKey', 'activationId']
#         properties_names = ['all']
#         #_GetPropertyList()
#         #target_objects = []
#         #for task in task_manager.recentTask:
#         #    return [property.name for property in task.info._GetPropertyList()]
#         #return
#         #properties_names = self.object_properties_names(object_type)
#         #properties_names.remove('type')
#         #return properties_names
#
#         #taskManager = content.taskManager
#         # properties_names.remove('activationId')
#         # properties_names.remove('rootTaskKey')
#         # properties_names.remove('parentTaskKey')
#         return self.get_objects_properties(object_type, target_objects, properties_names)
#
# #        task_filter_spec_by_entity = pyVmomi.vim.TaskFilterSpec.ByEntity(entity=entity)
# #        filterspec = pyVmomi.vim.TaskFilterSpec(entity=task_filter_spec_by_entity)
# #        #return task_filter_spec_by_entity
# #        collector = taskManager.CreateCollectorForTasks(filterspec)
#
# #        filterspec = pyVmomi.vim.TaskFilterSpec(entity=pyVmomi.vim.TaskFilterSpec.ByEntity(entity=entity, recursion="children"))
# #        collector = taskManager.CreateCollectorForTasks(filterspec)
#         #byEntity = pyVmomi.vim.event.TaskFilterSpec.ByEntity(entity=entity)
# #        ids = []
# #        filterSpec = pyVmomi.vim.event.TaskFilterSpec(entity=byEntity, eventTypeId=ids)
# #        eventManager = self.content().taskManager
# #       events = eventManager.QueryEvent(filterSpec)
#
#         # import datetime
#         # time = datetime.datetime.now()
#         # time2 = time - datetime.timedelta(hours=1)
#         #
#         # tfs = pyVmomi.vim.TaskFilterSpec(entity=byEntity, userName=None, alarm=None, scheduledTask=None)
#         #
#         # tc = self.content().taskManager.CreateCollectorForTasks(tfs)
#         # tlist = tc.ReadNextTasks(maxCount=100)
#
#         taskManager = self.content().taskManager
#         pyVmomi.vim.TaskFilterSpec()
#         #tasks = taskManager.CreateCollectorForTasks(pyVmomi.vim.TaskFilterSpec())
#         #tasks.ResetCollector()
#         #alltasks = tasks.ReadNextTasks(999)
#         #yesterday = datetime.now() - timedelta(1)
#         return "collector"
#         #return self.get_objects_properties(object_type, target_objects, properties_names)

    def tasks_recent(self):
        tasks = []
        task_manager = self.content().taskManager
        for task in task_manager.recentTask:                # will make a REST call per task
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

    def datastore(self, name=None):
        return self.get_objects_Datastore().pop()
    
    def get_datastore_by_name(self, dc, name): # dc is datacenter
        """
        Pick a datastore by its name.
        """
        for ds in dc.datastore:
            try:
                if ds.name == name:
                    return ds
            except:  # Ignore datastores that have issues
                pass
        raise Exception("Failed to find %s on datacenter %s" % (name, dc.name))
    
    def get_largest_free_ds(self, dc):
        """
        Pick the datastore that is accessible with the largest free space.
        """
        largest = None
        largestFree = 0
        for ds in dc.datastore:
            try:
                freeSpace = ds.summary.freeSpace
                if freeSpace > largestFree and ds.summary.accessible:
                    largestFree = freeSpace
                    largest = ds
            except:  # Ignore datastores that have issues
                pass
        if largest is None:
            raise Exception('Failed to find any free datastores on %s' % dc.name)
        return largest

    def folders(self):
        folders = []
        for child in self.content().rootFolder.childEntity:     # todo: add better support for datacenter
            datacenter = child                                  # this code assumes that this node is an of type 'vim.Datacenter:ha-datacenter'
            if hasattr(datacenter, 'vmFolder'):                 # if it has folders addit
                folders.append(datacenter.vmFolder)             # todo: add support for nested folders (see code at https://github.com/vmware/pyvmomi/blob/master/sample/getallvms.py#L58 )
        return folders

    def get_object(self, vim_type, name=None):
        content = self.content()

        container = content.viewManager.CreateContainerView(content.rootFolder, [vim_type], True)
        for object in container.view:
            if name is None:                            # if no name is provided return the first one
                return object
            if object.name == name:
                return object

    def get_object_folder         (self, name): return self.get_object(pyVmomi.vim.Folder        , name)
    def get_object_network        (self, name): return self.get_object(pyVmomi.vim.Network       , name)
    def get_object_virtual_machine(self, name): return self.get_object(pyVmomi.vim.VirtualMachine, name)

    def get_objects(self, objects_types=None):
        if objects_types is not list:
            if objects_types is not None:
                objects_types = [objects_types]
            else:
                objects_types = []
        target = self.content().rootFolder
        return self.get_objects_from(target, objects_types)

    def get_objects_from(self, target, objects_types=None):
        container = self.content().viewManager.CreateContainerView(target, objects_types, True)
        return container.view

    def get_objects_properties(self, object_type, target_objects, properties_names):
        property_filter_spec = self.object_filter_spec(object_type, target_objects, properties_names)
        return self.get_objects_properties_using_filter_spec(property_filter_spec)

    def get_objects_properties_using_filter_spec(self, property_filter_spec):
        property_collector = self.property_collector()
        retrieve_options   = pyVmomi.vmodl.query.PropertyCollector.RetrieveOptions()
        results            = property_collector.RetrievePropertiesEx([property_filter_spec], retrieve_options)
        objects_properties = {}
        for object in results.objects:
            object_id         = f"vim.{object.obj._wsdlName}:{object.obj._moId}"        # use the id of the object as the key (since we already have the object.obj value from the query)
            object_properties = {}
            for property in object.propSet:
                object_properties[property.name] = property.val
            objects_properties[object_id] = object_properties
        return objects_properties

    def get_objects_Compute_Resources(self): return self.get_objects(pyVmomi.vim.ComputeResource)
    def get_objects_Datacenters      (self): return self.get_objects(pyVmomi.vim.Datacenter     )
    def get_objects_Datastore        (self): return self.get_objects(pyVmomi.vim.Datastore      )
    def get_objects_Folders          (self): return self.get_objects(pyVmomi.vim.Folder         )

    def get_objects_Hosts            (self): return self.get_objects(pyVmomi.vim.HostSystem     )
    def get_objects_Networks         (self): return self.get_objects(pyVmomi.vim.Network        )
    def get_objects_ResourcePools    (self): return self.get_objects(pyVmomi.vim.ResourcePool   )
    def get_objects_StoragePods      (self): return self.get_objects(pyVmomi.vim.StoragePod     )
    def get_objects_Virtual_Machines (self): return self.get_objects(pyVmomi.vim.VirtualMachine )

    def object_filter_spec(self, object_type, target_objects, properties):
        objects_specs = []
        for object in target_objects:
            object_spec = pyVmomi.vmodl.query.PropertyCollector.ObjectSpec(obj=object)
            objects_specs.append(object_spec)

        propSet = pyVmomi.vmodl.query.PropertyCollector.PropertySpec(all=False)
        propSet.type = object_type
        propSet.pathSet = properties

        filterSpec = pyVmomi.vmodl.query.PropertyCollector.FilterSpec()
        filterSpec.objectSet = objects_specs
        filterSpec.propSet = [propSet]
        return filterSpec

    def object_methods_names(self, object_type):
        object = self.get_object(object_type)
        if object:
            methods_list = object._GetMethodList()
            return [method.name for method in methods_list]

            #return list(object._methodInfo.keys()) #_GetMethodList

    def object_properties_names(self, object_type):
        object = self.get_object(object_type)
        if object:
            properties_list = object._GetPropertyList()
            return [property.name for property in properties_list]

    def property_collector(self):
        return self.content().propertyCollector

    def resource_pool(self):
        hosts =  self.datacenter().hostFolder.childEntity
        for host in hosts:
            if hasattr(host, 'resourcePool'):
                return host.resourcePool
    
    def get_resource_pool_by_name(self, si, dc, name):
        """
        Get a resource pool in the datacenter by its names.
        """
        viewManager = si.content.viewManager
        containerView = viewManager.CreateContainerView(dc, [vim.ResourcePool],
                                                        True)
        try:
            for rp in containerView.view:
                if rp.name == name:
                    return rp
        finally:
            containerView.Destroy()
        raise Exception("Failed to find resource pool %s in datacenter %s" %
                        (name, dc.name))

    def get_largest_free_rp(self, si, dc):
        """
        Get the resource pool with the largest unreserved memory for VMs.
        """
        viewManager = si.content.viewManager
        containerView = viewManager.CreateContainerView(dc, [vim.ResourcePool],
                                                        True)
        largestRp = None
        unreservedForVm = 0
        try:
            for rp in containerView.view:
                if rp.runtime.memory.unreservedForVm > unreservedForVm:
                    largestRp = rp
                    unreservedForVm = rp.runtime.memory.unreservedForVm
        finally:
            containerView.Destroy()
        if largestRp is None:
            raise Exception("Failed to find a resource pool in dc %s" % dc.name)
        return largestRp

    def vm(self, vm_name):
        vm = self.get_object_virtual_machine(vm_name)
        if vm:
            return VM(vm)

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