import pyVmomi

from k8_vmware.vsphere.Sdk import Sdk


class Network:

    def __init__(self):
        self.sdk = Sdk()

    def get_host(self):                         # assume there is only one host
        hosts = self.sdk.get_objects_Hosts()
        assert len(hosts) == 1                  # throw exception if there is more than one host
        return hosts.pop()

    def networks(self):
        return self.sdk.get_objects_Networks()

    def networks_names(self):
        names = []
        for network in self.sdk.get_objects_Networks():
            names.append(network.name)
        return names

    def virtual_switches(self):
        switches = []
        for host in self.sdk.get_objects_Hosts():
            for switch in host.config.network.vswitch:
                switches.append(switch)
        return switches


    def port_group_create(self, name, vswitch_name, vlan=0, promiscuous=False):
        host            = self.get_host()
        policy          = pyVmomi.vim.host.NetworkPolicy()
        policy.security = pyVmomi.vim.host.NetworkPolicy.SecurityPolicy()
        policy.security.allowPromiscuous = bool(promiscuous)
        policy.security.macChanges       = False
        policy.security.forgedTransmits  = False
        spec = pyVmomi.vim.host.PortGroup.Specification(name=name, vlanId=int(vlan),
                                                        vswitchName=vswitch_name,
                                                        policy=policy)
        host.configManager.networkSystem.AddPortGroup(spec)
        return self.sdk.get_object_network(name)

    def port_group_exists(self, name):
        return name in self.networks_names()

    def port_group_not_exists(self, name):
        return self.port_group_exists(name) == False

    def port_group_delete(self, name):
        host = self.get_host()
        host.configManager.networkSystem.RemovePortGroup(name)

