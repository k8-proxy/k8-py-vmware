from os import environ
from dotenv import load_dotenv

class Config():

    def __init__(self):
        load_dotenv()

    def vsphere_host(self):
        return self.vsphere_server_details().get('host')

    def vsphere_server_details(self):
        return {
                    "host"    : environ.get('VSPHERE_HOST'),
                    "username": environ.get('VSPHERE_USERNAME'),
                    "password": environ.get('VSPHERE_PASSWORD')
                }

    def vsphere_set_server_details(self, host=None, username=None, password=None):
        if host:
            environ['VSPHERE_HOST'] = host
        if username:
            environ['VSPHERE_USERNAME'] = username
        if password:
            environ['VSPHERE_PASSWORD'] = password
        return self.vsphere_server_details()

    def vm_account(self):
        return  {
                    "username": environ.get('VM_USERNAME'),
                    "password": environ.get('VM_PASSWORD')
                }

    def esxi_ssh_config(self):
        return  {
                    "ssh_host": environ.get('VSPHERE_HOST'     ),
                    "ssh_user": environ.get('ESXI_SSH_USER'    ),
                    "ssh_key" : environ.get('ESXI_SSH_KEY'     ),
                }