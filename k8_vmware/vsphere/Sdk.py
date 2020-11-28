import  ssl

import pyVmomi
import  urllib3
import  warnings
from    pyVim import connect

from k8_vmware.Config import Config


class Sdk:
    def __init__(self):
        self._service_instance = None

    def server_details(self):
        return Config().vsphere_server_details()

    def unverified_ssl_context(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        warnings.simplefilter("ignore", ResourceWarning)
        sslContext = ssl._create_unverified_context()
        return sslContext

    def service_instance(self):
        server      = self.server_details()
        host        = server['host']
        user        = server['username']
        pwd         = server['password']
        ssl_context = self.unverified_ssl_context()
        try:
            if (self._service_instance is None):
                self.service_instance = connect.SmartConnect(host=host, user=user, pwd=pwd, sslContext=ssl_context)
        except Exception as exception:
            if(exception._wsdlName == 'InvalidLogin'):
                raise Exception(f"[vsphere][sdk] login failed for user {user}")
            else:
                raise exception

