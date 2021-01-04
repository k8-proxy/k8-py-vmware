from pprint import pprint
from unittest import TestCase

from osbot_utils.testing.Catch import Catch

from k8_vmware.helpers.TestCase_VM import TestCase_VM
from k8_vmware.helpers.View_Soap_Calls import View_Soap_Calls
from k8_vmware.vsphere.Sdk import Sdk
from pyVmomi import pyVmomi
from k8_vmware.vsphere.VM import VM


class test_Sdk(TestCase_VM):
    vm_name = f"tests__unit__" + __name__

    def setUp(self):
        self.sdk = Sdk()

    def test_about(self):
        content = self.sdk.about()
        assert content.vendor                == "VMware, Inc."
        assert content.version               == "6.7.0"
        assert content.licenseProductName    == "VMware ESX Server"
        assert content.licenseProductName    == "VMware ESX Server"
        assert content.licenseProductVersion == "6.0"

    def test_file_info(self):
        datastore_path = 'an data store'
        vmx_file = self.sdk.file_info(datastore_path)
        assert vmx_file.vmPathName == datastore_path

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

    def test_find_by_name(self):
        assert self.sdk.find_by_name(self.vm_name).name() == self.vm_name
        assert self.sdk.find_by_name("AAA_BBB_CCC") is None


    def test_find_by_ip(self):
        for vm in self.sdk.vms():
            ip = vm.ip()
            if ip:
                assert self.sdk.find_by_ip(ip).ip() == ip
                return
        print("Warning test ESX server had no VMs with IPs")

    def test_find_by_uuid(self):
        uuid = self.vm.uuid()
        assert self.sdk.find_by_uuid(uuid).uuid() == uuid

    def test_get_object(self):
        with View_Soap_Calls():
            name = self.vm.name()
            vm   = self.sdk.get_object(pyVmomi.vim.VirtualMachine,name)
            pprint(vm)
            #assert vm.name == name

    def test_get_objects_Datastore(self):
        datastores = self.sdk.get_objects_Datastore()
        assert len(datastores) >0

    def test_get_object_virtual_machine(self):
        name = self.vm.name()
        vm   = VM(self.sdk.get_object_virtual_machine(name))
        assert vm.name() == name

    def test_get_objects(self):
        objects = self.sdk.get_objects()
        assert len(objects) > 0

    def test_get_objects_properties(self):

        target_objects = [self.vm.vm]                                            # use a temp vm to make sure we always have one
        object_type    = type(self.vm.vm)
        vm_id          = self.vm.id()

        properties_names = self.sdk.object_properties_names(object_type)
        results          = self.sdk.get_objects_properties(object_type, target_objects, properties_names)

        assert vm_id == f'vim.VirtualMachine:{self.vm.moid()}'
        assert vm_id in results
        assert len(results) == 1
        object_properties = results[vm_id]
        properties_names.remove('alarmActionsEnabled')          # these properties are not returned from the server
        properties_names.remove('parentVApp')
        properties_names.remove('snapshot')
        assert sorted(list(set(object_properties))) == sorted(properties_names)
        assert object_properties['name'] == self.vm.name()

        # to get properties from all current VMs use:
        #   target_objects = self.sdk.get_objects_Virtual_Machines()


    def test_folders(self):
        folders = self.sdk.folders()
        assert str(folders) == "['vim.Folder:ha-folder-vm']"

    def test_object_filter_spec(self):
        # see test_get_objects_properties
        pass

    def test_object_methods_names(self):
        object_type = pyVmomi.vim.VirtualMachine
        method_names = self.sdk.object_methods_names(object_type)
        assert method_names == ['SetCustomValue', 'Destroy', 'Reload','Rename',         # these ones where not in list(object._methodInfo.keys())
                                'AcquireMksTicket', 'AcquireTicket', 'Answer', 'ApplyEvcMode', 'AttachDisk', 'CheckCustomizationSpec', 'Clone', 'ConsolidateDisks', 'CreateScreenshot', 'CreateSecondaryEx',
                                'CreateSecondary', 'CreateSnapshotEx', 'CreateSnapshot', 'CryptoUnlock', 'Customize', 'DefragmentAllDisks', 'DetachDisk', 'DisableSecondary', 'DropConnections', 'EnableSecondary',
                                'EstimateStorageRequirementForConsolidate', 'ExportVm', 'ExtractOvfEnvironment', 'InstantClone', 'MakePrimary', 'MarkAsTemplate', 'MarkAsVirtualMachine', 'Migrate', 'MountToolsInstaller',
                                'PowerOff', 'PowerOn', 'PromoteDisks', 'PutUsbScanCodes', 'QueryChangedDiskAreas', 'QueryConnections', 'QueryFaultToleranceCompatibility', 'QueryFaultToleranceCompatibilityEx',
                                'QueryUnownedFiles', 'RebootGuest', 'Reconfigure', 'RefreshStorageInfo', 'Relocate', 'RemoveAllSnapshots', 'ResetGuestInformation', 'Reset', 'RevertToCurrentSnapshot', 'SendNMI',
                                'SetDisplayTopology', 'SetScreenResolution', 'ShutdownGuest', 'StandbyGuest', 'StartRecording', 'StartReplaying', 'StopRecording', 'StopReplaying', 'Suspend', 'TerminateFaultTolerantVM',
                                'Terminate', 'TurnOffFaultTolerance', 'UnmountToolsInstaller', 'Unregister', 'UpgradeTools', 'UpgradeVirtualHardware', 'ReloadFromPath']

        datastore_methods = self.sdk.object_methods_names(pyVmomi.vim.Datastore)

        assert datastore_methods == ['SetCustomValue', 'Destroy', 'Reload', 'Rename', 'EnterMaintenanceMode', 'ExitMaintenanceMode', 'DestroyDatastore', 'Refresh', 'RefreshStorageInfo',
                                    'RenameDatastore', 'UpdateVVolVirtualMachineFiles', 'UpdateVirtualMachineFiles']

    def test_object_properties_names(self):
        object_type = pyVmomi.vim.VirtualMachine

        properties_names = self.sdk.object_properties_names(object_type)
        assert properties_names == ['value', 'availableField', 'parent', 'customValue', 'overallStatus', 'configStatus', 'configIssue', 'effectiveRole', 'permission', 'name', 'disabledMethod', 'recentTask',
                                    'declaredAlarmState', 'triggeredAlarmState', 'alarmActionsEnabled', 'tag', 'capability', 'config', 'layout', 'layoutEx', 'storage', 'environmentBrowser', 'resourcePool',
                                    'parentVApp', 'resourceConfig', 'runtime', 'guest', 'summary', 'datastore', 'network', 'snapshot', 'rootSnapshot', 'guestHeartbeatStatus']

        datastore_properties = self.sdk.object_properties_names(pyVmomi.vim.Datastore)
        assert datastore_properties == ['value', 'availableField', 'parent', 'customValue', 'overallStatus', 'configStatus', 'configIssue', 'effectiveRole', 'permission', 'name', 'disabledMethod', 'recentTask',
                                        'declaredAlarmState', 'triggeredAlarmState', 'alarmActionsEnabled', 'tag', 'info', 'summary', 'host', 'vm', 'browser', 'capability', 'iormConfiguration']

    def test_vms(self):
        vms = self.sdk.vms()
        assert len(vms) > 0

    def test_names(self):
        names = self.sdk.vms_names()
        assert len(names) > 0

    def test_service_instance(self):
        service_instance = self.sdk.service_instance()
        assert service_instance.content.about.apiVersion         == '6.7.3'
        assert service_instance.content.about.licenseProductName == 'VMware ESX Server'
        assert service_instance.content.about.osType             == 'vmnix-x86'

    # def test_dump_json(self):
    #
    #     obj_type = "VirtualMachine"
    #     moid     = self.vm.moid()
    #
    #     json_dump = self.sdk.json_dump(obj_type, moid)
    #     json_data = json.loads(json_dump)
    #     assert json_data['_vimid'  ] == moid
    #     assert json_data['_vimtype'] == "vim.VirtualMachine"


    # todo: fix experiment (see tasks_recent_experiment)
    def test_tasks(self):               # todo: find better way to do this since when running multiple tests the self.sdk.tasks_recent() can take multiple seconds to execute
        #with View_Soap_Calls():
        # with Catch():
        #     #pprint(self.sdk.get_objects())
        #     self.sdk.find_by_ip('aaaaaa')
        #     recent_tasks    = self.sdk.tasks_recent(self.vm.vm)
        #     pprint(recent_tasks)
        #     return
        self.sdk.find_by_ip('aaaaaa')
        recent_tasks = self.sdk.tasks_recent()
        most_recent_one = recent_tasks.pop()

        assert most_recent_one['DescriptionId'] == 'SearchIndex.findByIp'
        assert most_recent_one['Key'          ] == f"haTask--vim.SearchIndex.findByIp-{most_recent_one['EventChainId']}"
        assert most_recent_one['State'        ] == 'success'
        assert most_recent_one['Entity'       ] == 'None'
