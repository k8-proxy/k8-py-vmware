from pprint import pprint
from unittest import TestCase

import pytest
from osbot_utils.utils.Misc import random_string
from pytest import skip

from k8_vmware.helpers.Sdk_User import Sdk_User
from k8_vmware.helpers.for_osbot_utils.Misc import random_password
from k8_vmware.vsphere.ESX_Cli import ESX_Cli
from k8_vmware.vsphere.Sdk import Sdk


class test_ESX_Cli(TestCase):
    @classmethod

    def setUpClass(cls) -> None:
        cls.esx_cli     = ESX_Cli()
        cls.user_id     = f"user_{random_string()}"
        cls.password    = random_password()
        cls.role        = 'Admin'
        cls.description = f"description_{random_string()}"

        #print('****')
        #print('user', cls.user_id)
        #print('password', cls.password)

        assert cls.esx_cli.system_account_create(cls.user_id, cls.password, cls.description) == ''
        assert cls.esx_cli.system_permission_set(cls.user_id, cls.role) == ''
        #assert cls.user_id in set(cls.esx_cli.system_account_list(index_by='UserID'))
        #print("user created ok")


    @classmethod
    def tearDownClass(cls) -> None:
        # remove user
        assert cls.esx_cli.system_account_remove(cls.user_id) == ''
        assert cls.esx_cli.system_account_remove(cls.user_id) == f"The user or group named '{cls.user_id}' does not exist."

    def setUp(self) -> None:
        pass

    def test_exec(self):
        assert "Usage: esxcli [options] {namespace}+ {cmd} [cmd options]" in self.esx_cli.exec('')

    def test_esxcli_json(self):
        assert set(self.esx_cli.exec_return_json('network ip dns server list')) == {'DNSServers'}

    def test_system_account_create(self):                                                                       # note: setUpClass  will create and user with the id self.user_id
        assert self.user_id in set(self.esx_cli.system_account_list(index_by='UserID'))                         # confirm user exists
        with Sdk_User(user_id=self.user_id, password=self.password) as sdk_user:                                # login to server with the temp user
            assert sdk_user.login_result is True                                                                # confirm login was ok
            assert Sdk().about_name() == 'VMware ESXi'                                                          # confirms we are able to login and make calls to the SOAP API

        assert self.esx_cli.system_account_create(self.user_id, self.password, self.description) == f"The specified key, name, or identifier '{self.user_id}' already exists."

    def test_system_account_list(self):
        users = self.esx_cli.system_account_list(index_by='UserID')
        assert self.user_id  in set(users)
        assert set(users[self.user_id]) == {'Description', 'UserID'}


    def test_system_account_set(self):
        #change user details
        new_description = f"description_{random_string()}"
        new_password    = random_password()

        assert self.esx_cli.system_account_set(self.user_id, new_password, new_description) == ''
        user = self.esx_cli.system_account_list(index_by='UserID').get(self.user_id)

        assert user == {"Description" : new_description , "UserID" : self.user_id}

        with Sdk_User(user_id=self.user_id, password=new_password) as sdk_user:
            assert sdk_user.login_result is True

    def test_system_permission_unset(self):
        assert self.esx_cli.system_permission_unset(self.user_id) == ''                                         # remove user role
        assert self.user_id not in self.esx_cli.system_permission_list(index_by="Principal").keys()             # confirm user is not there
        assert self.esx_cli.system_permission_set(self.user_id, self.role) == ''                                # add back user role
        assert self.user_id in self.esx_cli.system_permission_list(index_by="Principal").keys()                 # confirm user is there

    def test_system_hostname_get(self):
        assert sorted(set(self.esx_cli.system_hostname_get())) == ['DomainName', 'FullyQualifiedDomainName', 'HostName']

    def test_system_permission_list(self):
        assert self.user_id in self.esx_cli.system_permission_list(index_by="Principal").keys()

    def test_system_stats_installtime_get(self):
        date = self.esx_cli.system_stats_installtime_get()
        assert date.year == 2020

    def test_system_version_get(self):
        assert set(self.esx_cli.system_version_get()) == {'Product', 'Patch', 'Version', 'Update', 'Build'}


