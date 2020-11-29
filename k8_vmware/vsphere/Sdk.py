import atexit
import  ssl

import pyVmomi
import  urllib3
import  warnings
from    pyVim import connect
from pyVim.connect import Disconnect

from k8_vmware.Config import Config


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

    def service_instance(self):
        server      = self.server_details()
        host        = server['host']
        user        = server['username']
        pwd         = server['password']
        ssl_context = self.unverified_ssl_context()
        try:
            print('[service_instance]')
            if (Sdk.cached_service_instance is None):
                print(" >>> Logging in")
                Sdk.cached_service_instance = connect.SmartConnect(host=host, user=user, pwd=pwd, sslContext=ssl_context)
                atexit.register(Disconnect, self.service_instance)
            else:
                print(" >>> using cached version")
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
            if hasattr(datacenter, 'vmFolder'):                 # if it has folders
                folders.append(datacenter.vmFolder)             # add it
        return folders

    def vms(self):
        vms = []

        for folder in self.folders():
            for vm in folder.childEntity:
                vms.append(vm)
        return vms