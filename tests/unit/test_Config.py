from unittest import TestCase

from k8_vmware.Config import Config


class test_Config(TestCase):

    def setUp(self) -> None:
        self.config = Config()

    def test_vsphere_server(self):
        server_details = self.config.vsphere_server_details()
        assert server_details.get('host'    ) is not None
        assert server_details.get('username') is not None
        assert server_details.get('password') is not None
        print(server_details)