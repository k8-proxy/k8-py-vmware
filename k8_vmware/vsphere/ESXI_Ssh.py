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

    def esxcli(self, cli_command, **kwargs):
        for key in kwargs:
            value = kwargs[key]
            if value:
                cli_command += f' -{key}="{value}"'
        return self.exec("esxcli " + cli_command)

    # formatters available: xml, csv, keyvalue, python, json , html, table , simple ("tree" doesn't seem to be avaible in the current test server)
    def esxcli_format_output(self, formatter, cli_command, **kwargs):
        return self.esxcli(f"--debug --formatter={formatter} {cli_command}", **kwargs)

    def esxcli_date(self, cli_command):
        date_time_str = self.esxcli(cli_command)
        return datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S')            # convert string with date to an actual datetime object

    @index_by
    @group_by
    def esxcli_json(self, cli_command, **kwargs):
        json_data = self.esxcli_format_output("json",  cli_command, **kwargs)
        return json.loads(json_data)

    # since we already have the json formatter, there doesn't seem to be a good case for also getting data in csv

    #def esxcli_output_csv(self, cli_command):
    #    csv_data = self.esxcli("--formatter=csv " + cli_command)

    # helper methods: esxcli commands  (see descriptions at https://www.altaro.com/vmware/top-20-esxcli-commands/)

    def esxcli_system_account_create        (self, user_id, password, description): return self.esxcli     ("system account add"          , d=description , i=user_id, p=password, c=password)
    def esxcli_system_account_list          (self, **kwars                       ): return self.esxcli_json("system account list"         , **kwars)
    def esxcli_system_account_set           (self, user_id, password, description): return self.esxcli     ("system account set"          , d=description , i=user_id, p=password, c=password)
    def esxcli_system_account_remove        (self, user_id                       ): return self.esxcli     ("system account remove "      , i=user_id)
    def esxcli_system_hostname_get          (self, **kwars                       ): return self.esxcli_json("system hostname get"         , **kwars)
    def esxcli_system_permission_list       (self, **kwars                       ): return self.esxcli_json("system permission list"      , **kwars)
    def esxcli_system_permission_set        (self, user_id, role                 ): return self.esxcli     ("system permission set"       , i=user_id, r=role)
    def esxcli_system_permission_unset      (self, user_id                       ): return self.esxcli     ("system permission unset"     , i=user_id        )
    def esxcli_system_stats_installtime_get (self, **kwars                       ): return self.esxcli_date("system stats installtime get", **kwars)
    def esxcli_system_version_get           (self, **kwars                       ): return self.esxcli_json("system version get"          , **kwars)

