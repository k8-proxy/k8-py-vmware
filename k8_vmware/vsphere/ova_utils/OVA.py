import time
import pyVmomi
from osbot_utils.utils import Http
from osbot_utils.utils.Files import file_not_exists
from k8_vmware.vsphere.ova_utils.OVF_Handler import OvfHandler
from k8_vmware.vsphere.Sdk import Sdk

class OVA:

    def __init__(self): # todo add methods to manipulated OVA files
        self.sdk = Sdk()

    def upload_ova(self, ova_path):
        sdk = self.sdk
        # assert file_exists(ova_path)
        # todo: add explicit check for file exists and return error
        # todo: normalise method return values
        ovf_handle = OvfHandler(ova_path)

        ovfManager = sdk.content().ovfManager
        rp = sdk.resource_pool()
        ds = sdk.datastore()
        dc = sdk.datacenter()
        cisp = pyVmomi.vim.OvfManager.CreateImportSpecParams()
        cisr = ovfManager.CreateImportSpec(ovf_handle.get_descriptor(), rp, ds, cisp)
        ovf_handle.set_spec(cisr)

        lease = rp.ImportVApp(cisr.importSpec, dc.vmFolder)
        while lease.state == pyVmomi.vim.HttpNfcLease.State.initializing:
            print("Waiting for lease to be ready...")
            time.sleep(1)

        if lease.state == pyVmomi.vim.HttpNfcLease.State.error:
            print("Lease error: %s" % lease.error)
            return -1

        if lease.state == pyVmomi.vim.HttpNfcLease.State.done:
            return 1

        host = sdk.server_details().get('host')

        print("Starting deploy...")
        result = ovf_handle.upload_disks(lease, host)
        return result

    def download_ova_file(self, url, target_ova_path):
        if file_not_exists(target_ova_path):
            Http.GET_bytes_to_file(url, target_ova_path)
        return target_ova_path