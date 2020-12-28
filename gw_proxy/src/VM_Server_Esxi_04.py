from pprint import pprint

from osbot_utils.utils.Misc import random_string

from k8_vmware.Config import Config
from k8_vmware.helpers.for_osbot_utils.Misc import random_password
from k8_vmware.vsphere.ESXI_Ssh import ESXI_Ssh
from k8_vmware.vsphere.ESX_Cli import ESX_Cli
from k8_vmware.vsphere.Sdk import Sdk

class VM_Server_Esxi_04:

    def __init__(self):
        self.sdk  = Sdk()
        self.esx_cli = ESX_Cli()
        self.server_details = Config().vsphere_server_details()

    def create_admin_user(self, user_id):

        password    = random_password()
        description = "admin user for server esxi04"
        self.esx_cli.system_account_remove(user_id)
        account_create = self.esx_cli.system_account_create(user_id, password, description)
        permission_set = self.esx_cli.system_permission_set(user_id, "Admin")
        return {
                    "account_create" : account_create ,
                    "description"    : description    ,
                    "permission_set" : permission_set ,
                    "password"       : password       ,
                    "user_id"        : user_id
                 }
