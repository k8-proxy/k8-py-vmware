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
        return self.service_instance().RetrieveContent().about

    def content(self):
        return self.service_instance().RetrieveContent()

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

    def folders(self):
        folders = []
        for child in self.content().rootFolder.childEntity:     # todo: add better support for datacenter
            datacenter = child                                  # this code assumes that this node is an of type 'vim.Datacenter:ha-datacenter'
            if hasattr(datacenter, 'vmFolder'):                 # if it has folders addit
                folders.append(datacenter.vmFolder)             # todo: add support for nested folders (see code at https://github.com/vmware/pyvmomi/blob/master/sample/getallvms.py#L58 )
        return folders

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