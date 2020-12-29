from os import environ
from pprint import pprint
from unittest import TestCase
from osbot_utils.utils.Misc import random_string
from pytest import skip

from k8_vmware.Config import Config
from k8_vmware.helpers.Sdk_User import Sdk_User
from k8_vmware.helpers.for_osbot_utils.Misc import random_password
from k8_vmware.vsphere.ESXI_Ssh import ESXI_Ssh
from k8_vmware.vsphere.Sdk import Sdk


class test_ESXI_Ssh(TestCase):

    def setUp(self) -> None:
        self.ssh        = ESXI_Ssh()
        self.ssh_config = self.ssh.ssh_config()
        self.ssh_user   = self.ssh_config.get('ssh_user')
        self.ssh_key    = self.ssh_config.get('ssh_key')
        if self.ssh_key is None:
            skip("Skipping test because environment variable ssh_host is not configured")

    # base methods
    def test_exec_ssh_command(self):
        assert self.ssh.exec_ssh_command(       ) == {'error': '', 'output': 'VMkernel\n', 'status': True}
        assert self.ssh.exec_ssh_command('uname') == {'error': '', 'output': 'VMkernel\n', 'status': True}
        assert self.ssh.exec_ssh_command('aaaa' ) == {'error': 'sh: aaaa: not found\n', 'output': '', 'status': False}

    def test_get_get_ssh_params(self):
        ssh_params = self.ssh.get_ssh_params('aaa')
        assert ssh_params == ['-t', '-i', environ.get('ESXI_SSH_KEY'),
                              environ.get('ESXI_SSH_USER') + '@' + environ.get('VSPHERE_HOST'),
                              'aaa']

    def test_exec(self):
        #self.ssh.exec('uname'        ) == 'VMkernel'
        self.ssh.exec('cd /bin ; pwd') == '/bin'

    def test_ssh_config(self):
        config = self.ssh.ssh_config()
        assert config['ssh_host'] == environ.get('VSPHERE_HOST'    )
        assert config['ssh_user'] == environ.get('ESXI_SSH_USER')
        assert config['ssh_key' ] == environ.get('ESXI_SSH_KEY'    )

    # helper methods

    def test_uname(self):
        assert self.ssh.uname() == 'VMkernel'

    def test_exec(self):
        assert 'Usage: esxcli system {cmd} [cmd options]' in self.ssh.exec('esxcli system') # you can also use this to see the commands avaiable in the `esxcli system` namespace

    # helper methods: esxcli




