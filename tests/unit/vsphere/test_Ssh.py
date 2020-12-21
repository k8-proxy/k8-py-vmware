from datetime import datetime
from os import environ
from pprint import pprint
from unittest import TestCase

from pytest import skip

from k8_vmware.vsphere.ESXI_Ssh import ESXI_Ssh

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
                              environ.get('VSPHERE_USERNAME') + '@' + environ.get('VSPHERE_HOST'),
                              'aaa']

    def test_exec(self):
        #self.ssh.exec('uname'        ) == 'VMkernel'
        self.ssh.exec('cd /bin ; pwd') == '/bin'

    def test_ssh_config(self):
        config = self.ssh.ssh_config()
        assert config['ssh_host'] == environ.get('VSPHERE_HOST'    )
        assert config['ssh_user'] == environ.get('VSPHERE_USERNAME')
        assert config['ssh_key' ] == environ.get('ESXI_SSH_KEY'    )

    # helper methods

    def test_uname(self):
        assert self.ssh.uname() == 'VMkernel'

    def test_pwd(self):
        #result = self.ssh.pwd()

        #pprint(self.ssh.exec('esxcli system version get'))
        pprint(self.ssh.exec('esxcli system'))
        #pprint(self.ssh.uname())

    # helper methods: esxcli

    def test_esxcli(self):
        assert "Usage: esxcli [options] {namespace}+ {cmd} [cmd options]" in self.ssh.esxcli('')

    def test_esxcli_json(self):
        set(self.ssh.esxcli_json('network ip dns server list')) == {'DNSServers'}

    def test_esxcli_system_account_list(self):
        users = self.ssh.esxcli_system_account_list(index_by='UserID')
        assert self.ssh_user  in set(users)
        assert set(users[self.ssh_user]) == {'Description', 'UserID'}

    def test_esxcli_system_hostname_get(self):
        assert sorted(set(self.ssh.esxcli_system_hostname_get())) == ['DomainName', 'FullyQualifiedDomainName', 'HostName']

    def test_esxcli_system_stats_installtime_get(self):
        date = self.ssh.esxcli_system_stats_installtime_get()
        assert date.year == 2020

    def test_esxcli_system_version_get(self):
        assert set(self.ssh.esxcli_system_version_get()) == {'Product', 'Patch', 'Version', 'Update', 'Build'}





