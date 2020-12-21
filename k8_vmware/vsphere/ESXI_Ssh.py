import json
from datetime import datetime

from osbot_utils.decorators.Lists import index_by, group_by
from osbot_utils.utils.Process import exec_process

from k8_vmware.Config import Config


class ESXI_Ssh:
    def __init__(self):
        pass

    # base methods
    def exec(self, command):
        result = self.exec_ssh_command(command)
        output = result['output'].strip()
        return output

    # def exec__return_dict(self, command):
    #     output = self.exec(command)
    #     data = {}
    #     for item in output.split('\n'):
    #         (key, value) = item.split(':', 1)
    #         data[key.strip()] = value.strip()
    #     return data

    def exec_ssh_command(self, command='uname'):
        result = exec_process("ssh", self.get_ssh_params(command))
        result['stderr'] = result['stderr'].replace('Pseudo-terminal will not be allocated because stdin is not a terminal.\r\n', '') # Note: ok to ignore this error
        if result['stderr'] and not result['stdout']:                                                                                 # add an simple execution status
            result['status'] = False
        else:
            result['status'] = True
        return {
                    "error"  : result['stderr'],
                    "output" : result['stdout'],
                    "status" : result['status']
        }
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
    def pwd  (self): return self.exec('pwd')   # not sure how useful this one is
    def uname(self): return self.exec('uname')

    # helper methods: esxcli (from https://www.altaro.com/vmware/top-20-esxcli-commands/)

    def esxcli(self, cli_command):
        return self.exec("esxcli " + cli_command)

    # formatters available: xml, csv, keyvalue, python, json , html, table , simple ("tree" doesn't seem to be avaible in the current test server)
    def esxcli_format_output(self, formatter, cli_command):
        return self.esxcli(f"--debug --formatter={formatter} {cli_command}")

    @index_by
    @group_by
    def esxcli_json(self, cli_command):
        json_data = self.esxcli_format_output("json",  cli_command)
        return json.loads(json_data)

    # since we already have the json formatter, there doesn't seem to be a good case for also getting data in csv

    #def esxcli_output_csv(self, cli_command):
    #    csv_data = self.esxcli("--formatter=csv " + cli_command)


    @index_by
    def esxcli_system_account_list(self):
        """
        Lists the local users created on the ESXi host.

        :return:
        """
        return self.esxcli_json("system account list")

    def esxcli_system_hostname_get(self):
        """
        Returns the hostname, domain and FQDN for the host.

        :return: dict with data
        """
        return self.esxcli_json("system hostname get")

    def esxcli_system_stats_installtime_get(self):
        """
         Returns the date and time of when ESXi was installed.

         return: datetime
        """
        date_time_str = self.exec("esxcli system stats installtime get")
        return datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S')            # convert string with date to an actual datetime object

    def esxcli_system_version_get(self):
        """
        Returns the ESXi build and version numbers

        :return: dict with data
        """
        return self.esxcli_json("system version get")

