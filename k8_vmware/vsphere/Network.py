import pyVmomi

from k8_vmware.vsphere.Sdk import Sdk


class Network:

    def __init__(self):
        self.sdk = Sdk()

    def list(self):
        return self.sdk.get_objects_Networks()

    def port_group_create(self, name, vswitch_name, vlan=0, promiscuous=False):
        policy = pyVmomi.vim.host.NetworkPolicy()
        policy.security = pyVmomi.vim.host.NetworkPolicy.SecurityPolicy()
        policy.security.allowPromiscuous = bool(promiscuous)
        policy.security.macChanges = False
        policy.security.forgedTransmits = False
        spec = pyVmomi.vim.host.PortGroup.Specification(name=name, vlanId=int(vlan),
                                                        vswitchName=vswitch_name,
                                                        policy=policy)
        self.host.configManager.networkSystem.AddPortGroup(spec)


