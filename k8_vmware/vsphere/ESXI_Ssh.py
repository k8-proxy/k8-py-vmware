import json
from datetime import datetime

from osbot_utils.decorators.Lists import index_by, group_by
from osbot_utils.utils.Process import exec_process

from k8_vmware.Config import Config


class ESXI_Ssh:
    def __init__(self):
        self.last_exec_result = None

    # base methods
    def exec(self, command):
        result = self.exec_ssh_command(command)
        output = result['output'].strip()
        return output

    def exec_ssh_command(self, command='uname'):
        result = exec_process("ssh", self.get_ssh_params(command))
        result['stderr'] = result['stderr'].replace('Pseudo-terminal will not be allocated because stdin is not a terminal.\r\n', '') # Note: ok to ignore this error
        if result['stderr'] and not result['stdout']:                                                                                 # add an simple execution status
            result['status'] = False
        else:
            result['status'] = True

        result = {                                          # improve result data structure and fields name
                    "error"  : result['stderr'],
                    "output" : result['stdout'],
                    "status" : result['status']
        }
        self.last_exec_result = result
        return result

    def get_ssh_params(self, command):
        ssh_config = self.ssh_config()
        ssh_params = []
        ssh_params.append('-t'                                                  )       # -t "Force pseudo-tty allocation" note: Using -tt will make the returned data to be ascii encoded which is not what we want
        ssh_params.extend(['-i', ssh_config['ssh_key' ]]                        )       # add ssh key to login as
        ssh_params.append(f"{ssh_config['ssh_user']}@{ssh_config['ssh_host']}"  )       # add target host name
        ssh_params.append(command                                               )       # add command to execute
        return ssh_params

    def ssh_config(self):
        return Config().esxi_ssh_config()

    # helper methods: Linux (todo: get correct version)
    def uname(self): return self.exec('uname')

    # helper methods: esxcli



