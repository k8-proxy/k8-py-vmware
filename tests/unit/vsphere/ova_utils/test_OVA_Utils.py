from urllib.request import urlopen

from k8_vmware.helpers.TestCase_OVA import TestCase_OVA
from k8_vmware.vsphere.ova_utils.OVA import OVA
from k8_vmware.vsphere.ova_utils.OVA_Utils import OVA_Utils
from k8_vmware.vsphere.ova_utils.OVF_Handler import Ovf_Hanlder


class test_OVA(TestCase_OVA):
    def setUp(self) -> None:
        self.ova         =   OVA()
        self.ovf_handler =   Ovf_Hanlder(self.ova_path)
        self.utils=OVA_Utils()


    def test_headers_to_dict(self):
        response = urlopen(self.url)
        response=self.utils._headers_to_dict(response=response)
        assert 'accept-ranges' in response

    def test_get_ovafilename_from_pattern(self):
        response=self.utils.get_ovafilename_from_pattern(self.ovf_handler.tarfile)
        assert response is not None
