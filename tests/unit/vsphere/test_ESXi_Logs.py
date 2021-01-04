from pprint import pprint
from unittest import TestCase

from osbot_utils.utils.Misc import split_lines

from k8_vmware.vsphere.ESXi_Logs import ESXi_Logs


class test_ESXi_Logs(TestCase):

    def setUp(self) -> None:
        self.esxi_logs = ESXi_Logs()

    def assert_log_size(self, function, size=10):
        assert len(split_lines(function(size))) == size

    def test_log_files(self):
        print()
        pprint(self.esxi_logs.log_files())

    def test_get_log_file(self):
        size = 2
        data = self.esxi_logs.get_log_file('auth', size)
        assert len(split_lines(data))== size



    def test_auth       (self): self.assert_log_size(self.esxi_logs.auth      )
    def test_hostd      (self): self.assert_log_size(self.esxi_logs.hostd     )
    def test_shell      (self): self.assert_log_size(self.esxi_logs.shell     )
    def test_syslog     (self): self.assert_log_size(self.esxi_logs.syslog    )
    def test_vmauthd    (self): self.assert_log_size(self.esxi_logs.vmauthd   )
    def test_vmkernel   (self): self.assert_log_size(self.esxi_logs.vmkernel  )
    def test_vmksummary (self): self.assert_log_size(self.esxi_logs.vmksummary)
    def test_vmkwarning (self): self.assert_log_size(self.esxi_logs.vmkwarning)
    def test_vobd       (self): self.assert_log_size(self.esxi_logs.vobd      )
    def test_vpxa       (self): self.assert_log_size(self.esxi_logs.vpxa      )
