import logging
import sys
import tarfile
import pyVmomi
import ssl

from osbot_utils.utils.Files import file_exists
from six.moves.urllib.request import Request, urlopen
from threading import Timer
from k8_vmware.vsphere.ova_utils.File_Handle import FileHandle
from k8_vmware.vsphere.ova_utils.Web_Handle import Web_Handle
from k8_vmware.vsphere.ova_utils.OVA_Utils import OVA_Utils

logger = logging.getLogger(__name__)

class Ovf_Hanlder:
    """
    OvfHandler handles most of the OVA operations.
    It processes the tarfile, matches disk keys to files and
    uploads the disks, while keeping the progress up to date for the lease.
    """
    def __init__(self, ovafile):
        """
        Performs necessary initialization, opening the OVA file,
        processing the files and reading the embedded ovf file.
        """
        self.utils        =     OVA_Utils()
        self.handle       =     self._create_file_handle(ovafile)
        self.tarfile      =     tarfile.open(fileobj=self.handle)
        ovffilename       =     self.utils.get_ovafilename_from_pattern(tarfile=self.tarfile)
        ovffile           =     self.tarfile.extractfile(ovffilename)
        self.descriptor   =     ovffile.read().decode()

    # def get_ovafilename(self,tarfile):
    #     ovffilename=list(filter(lambda x: x.endswith(".ovf"), tarfile.getnames()))[0]
    #ovffilename = list(filter(lambda x: x == fileItem.path,self.tarfile.getnames()))[0]
    #     return ovffilename

    def _create_file_handle(self, entry):
        """
        A simple mechanism to pick whether the file is local or not.
        This is not very robust.
        """
        if file_exists(entry):
            return FileHandle(entry)
        else:
            return Web_Handle(entry)

    def get_descriptor(self):
        return self.descriptor

    def set_spec(self, spec):
        """
        The import spec is needed for later matching disks keys with
        file names.
        """
        self.spec = spec

    def get_disk(self, fileItem, lease):
        """
        Does translation for disk key to file name, returning a file handle.
        """
        ovffilename=self.utils.get_ovffilename_from_path(tarfile=self.tarfile,path=fileItem.path)
        return self.tarfile.extractfile(ovffilename)

    def get_device_url(self, fileItem, lease):
        for deviceUrl in lease.info.deviceUrl:
            if deviceUrl.importKey == fileItem.deviceId:
                return deviceUrl
        raise Exception("Failed to find deviceUrl for file %s" % fileItem.path)

    def upload_disks(self, lease, host):
        """
        Uploads all the disks, with a progress keep-alive.
        """
        self.lease = lease
        try:
            self.start_timer()
            for fileItem in self.spec.fileItem:
                self.upload_disk(fileItem, lease, host)
            lease.Complete()
            logger.info("Finished deploy successfully.")
            return 0
        except pyVmomi.vmodl.MethodFault as e:
            logger.error("Hit an error in upload: %s" % e)
            lease.Abort(e)
        except Exception as e:
            logger.error("Lease: %s" % lease.info)
            logger.error("Hit an error in upload: %s" % e)
            lease.Abort(pyVmomi.vmodl.fault.SystemError(reason=str(e)))
            raise
        return -1

    def upload_disk(self, fileItem, lease, host):
        """
        Upload an individual disk. Passes the file handle of the
        disk directly to the urlopen request.
        """
        ovffile = self.get_disk(fileItem, lease)
        assert ovffile is not None

        deviceUrl   =    self.get_device_url(fileItem, lease)
        url         =    deviceUrl.url.replace('*', host)
        headers     =    {'Content-length': self.get_tarfile_size(ovffile)}

        sslContext  =    self.get_ssl_context()
        req         =    Request(url, ovffile, headers)
        self.request_urlopen(req, sslContext)

    def request_urlopen(self,req,sslContext):
        urlopen(req, context=sslContext)


    def get_ssl_context(self):
        if hasattr(ssl, '_create_unverified_context'):
            sslContext = ssl._create_unverified_context()
        else:
            sslContext = None
        return sslContext

    def start_timer(self):
        """
        A simple way to keep updating progress while the disks are transferred.
        """
        Timer(5, self.timer).start()

    def timer(self):
        """
        Update the progress and reschedule the timer if not complete.
        """
        try:
            prog = self.handle.progress()
            self.lease.Progress(prog)
            if self.lease.state not in [pyVmomi.vim.HttpNfcLease.State.done,
                                        pyVmomi.vim.HttpNfcLease.State.error]:
                self.start_timer()
            sys.stderr.write("Progress: %d%%\r" % prog)
        except:  # Any exception means we should stop updating progress.
            pass

    def get_tarfile_size(self,tarfile):
        """
        Determine the size of a file inside the tarball.
        If the object has a size attribute, use that. Otherwise seek to the end
        and report that.
        """
        if hasattr(tarfile, 'size'):
            return tarfile.size
        size = tarfile.seek(0, 2)
        tarfile.seek(0, 0)
        return size
