from unittest import TestCase
from k8_vmware.Config import Config
from k8_vmware.helpers.Sdk_User import Sdk_User
from k8_vmware.vsphere.Sdk import Sdk

class test_Sdk_User(TestCase):

    def setUp(self) -> None:
        self.config = Config()
        self.sdk    = Sdk()

    def test__enter__(self):
        server_details = self.config.vsphere_server_details()  # get server details (from env variables)
        with Sdk_User(user_id=server_details['username'] , password=server_details['password']) as sdk_user:
            assert self.sdk.login() is True
            assert sdk_user.login_result is True

        assert self.sdk.login() is True
        assert sdk_user.login_result is True

    def test__enter__bad_details(self):
        with Sdk_User(user_id='aaa', password='bbb') as sdk_user:
            assert sdk_user.login_result is False

        assert sdk_user.login_result is True
