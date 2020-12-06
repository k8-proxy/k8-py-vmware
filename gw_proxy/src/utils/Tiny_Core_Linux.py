from osbot_utils.utils       import Http
from osbot_utils.utils.Files import file_exists, file_not_exists

from k8_vmware.vsphere.Sdk import Sdk


class Tiny_Core_Linux:

    def __init__(self):
        self.url_core_iso  = 'https://distro.ibiblio.org/tinycorelinux/11.x/x86/release/Core-current.iso'
        self.path_core_iso = '/tmp/core-currenet.iso'
        self.vm_name       = 'tiny-core-linux'
        self.sdk           = Sdk()

    def create_vm(self):
        self.sdk.content()
        print('-----')
        vm = self.sdk.vm(self.vm_name)
        print('-----')
        #if vm is None:
        #    print('need to create vm')
        #print(f"VM: {vm}")
        pass

    def download_iso(self):
        if file_not_exists(self.path_core_iso):
            Http.GET_bytes_to_file(self.url_core_iso, self.path_core_iso)
        return self.path_core_iso