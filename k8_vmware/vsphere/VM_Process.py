import pyVmomi
import requests
from osbot_utils.utils.Misc import random_string

from k8_vmware.Config import Config
from k8_vmware.vsphere.Sdk import Sdk


class VM_Process:
    def __init__(self, vm):
        self.sdk            = Sdk()
        self.vm             = vm
        self.vm_account     = Config().vm_account()
        self.server_details = Config().vsphere_server_details()
        self.vm_user_name   = self.vm_account['username']
        self.vm_password    = self.vm_account['password']
        self.ip_server      = self.server_details['host']


    def exec(self, program_path, arguments):
        return self.start_process_return_stdout(program_path, arguments)

    def ls(self, path=""):
        return self.exec('/bin/ls', path)

    def start_process_return_stdout(self, program_path, arguments):
        content = self.sdk.content()
        # assert self.vm.guest().toolsStatus == 'toolsOk'

        file_stdout   = f"/tmp/_vm_exec_{random_string()}"
        arguments    += f" > {file_stdout}"        # capture stdout in a file
        creds         = pyVmomi.vim.vm.guest.NamePasswordAuthentication(username=self.vm_user_name, password=self.vm_password)
        pm            = content.guestOperationsManager.processManager
        ps            = pyVmomi.vim.vm.guest.ProcessManager.ProgramSpec(programPath=program_path, arguments=arguments)
        res           = pm.StartProgramInGuest(self.vm.vm, creds, ps)
        file_transfer = content.guestOperationsManager.fileManager.InitiateFileTransferFromGuest(self.vm.vm, creds, file_stdout)
        file_url      = file_transfer.url.replace("*:443", self.ip_server)
        resp          = requests.get(file_url, verify=False)
        return resp.text