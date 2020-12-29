import json
from datetime import datetime

from osbot_utils.decorators.Lists import index_by, group_by

from k8_vmware.vsphere.ESXI_Ssh import ESXI_Ssh


class ESX_Cli():

    def __init__(self):
        self.esxi_ssh = ESXI_Ssh()

    def exec(self, cli_command, **kwargs):
        for key in kwargs:
            value = kwargs[key]
            if value:
                cli_command += f' -{key}="{value}"'
        return self.esxi_ssh.exec("esxcli " + cli_command)

    # formatters available: xml, csv, keyvalue, python, json , html, table , simple ("tree" doesn't seem to be avaible in the current test server)
    def exec_return_formatted(self, formatter, cli_command, **kwargs):
        return self.exec(f"--debug --formatter={formatter} {cli_command}", **kwargs)

    def exec_return_date(self, cli_command):
        date_time_str = self.exec(cli_command)
        return datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S')            # convert string with date to an actual datetime object

    @index_by
    @group_by
    def exec_return_json(self, cli_command, **kwargs):
        json_data = self.exec_return_formatted("json", cli_command, **kwargs)
        return json.loads(json_data)

    # since we already have the json formatter, there doesn't seem to be a good case for also getting data in csv

    #def esxcli_output_csv(self, cli_command):
    #    csv_data = self.esxcli("--formatter=csv " + cli_command)

    # helper methods: esxcli commands  (see descriptions at https://www.altaro.com/vmware/top-20-esxcli-commands/)

    def network_firewall_get          (self, **kwars                       ): return self.exec_return_json("network firewall get"         , **kwars           )
    def network_firewall_ruleset_list (self, **kwars                       ): return self.exec_return_json("network firewall ruleset list", **kwars           )
    def network_ip_interface_ipv4_get (self, **kwars                       ): return self.exec_return_json("network ip interface ipv4 get", **kwars           )

    def system_account_create         (self, user_id, password, description): return self.exec            ("system account add"           , d=description , i=user_id, p=password, c=password)
    def system_account_list           (self, **kwars                       ): return self.exec_return_json("system account list"          , **kwars           )
    def system_account_set            (self, user_id, password, description): return self.exec            ("system account set"           , d=description , i=user_id, p=password, c=password)
    def system_account_remove         (self, user_id                       ): return self.exec            ("system account remove"        , i=user_id         )
    def system_hostname_get           (self, **kwars                       ): return self.exec_return_json("system hostname get"          , **kwars           )
    def system_permission_list        (self, **kwars                       ): return self.exec_return_json("system permission list"       , **kwars           )
    def system_permission_set         (self, user_id, role                 ): return self.exec            ("system permission set"        , i=user_id, r=role )
    def system_permission_unset       (self, user_id                       ): return self.exec            ("system permission unset"      , i=user_id         )
    def system_stats_installtime_get  (self, **kwars                       ): return self.exec_return_date("system stats installtime get" , **kwars           )
    def system_version_get            (self, **kwars                       ): return self.exec_return_json("system version get"           , **kwars           )


