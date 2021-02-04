from unittest import TestCase

class TestCase_OVA(TestCase):
    url="https://packages.vmware.com/photon/4.0/Beta/ova/photon-hw11-4.0-d98e681.ova"
    ova_path="./test.ova"
    vm_name = "Photon OS"

    @classmethod
    def setUpClass(cls) -> None:
        cls.url: str = cls.url
        cls.ova_path: str = cls.ova_path
        cls.vm_name: str = cls.vm_name

    @classmethod
    def tearDownClass(cls) -> None:
        pass