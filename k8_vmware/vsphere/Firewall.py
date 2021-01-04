import json
from pprint import pprint

from osbot_utils.decorators.lists.group_by import group_by
from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.utils.Json import json_round_trip

from k8_vmware.vsphere.Sdk import Sdk


class Firewall:
    def __init__(self):
        self.sdk = Sdk()

    def hosts(self):
        return self.sdk.get_objects_Hosts()

    @group_by
    @index_by
    def rules(self):
        rules = []
        for host in self.hosts():
            for ruleset in host.configManager.firewallSystem.firewallInfo.ruleset:
                for ruleset_rule in ruleset.rule:
                    pprint(ruleset)
                    pprint(ruleset_rule)
                    rule = {
                        "allow_all_ips"       : ruleset.allowedHosts.allIp                      ,
                        "allow_ip_addresses"  : json_round_trip(ruleset.allowedHosts.ipNetwork) ,
                        "allow_ip_networks"   : json_round_trip(ruleset.allowedHosts.ipAddress) ,
                        "enabled"             : ruleset.enabled                                 ,
                        "direction"           : ruleset_rule.direction                          ,
                        "key"                 : ruleset.key                                     ,
                        "label"               : ruleset.label                                   ,
                        "port"                : ruleset_rule.port                               ,
                        "port_end"            : ruleset_rule.endPort                            ,
                        "port_type"           : ruleset_rule.portType                           ,
                        "protocol"            : ruleset_rule.protocol                           ,
                        "required"            : ruleset.required                                ,
                        "service"             : ruleset.service
                    }
                    rules.append(rule)
                    #return rules
        return rules
                #print(rule)
                #return ruleset_rule
                #return rule