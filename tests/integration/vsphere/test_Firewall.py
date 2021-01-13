from pprint import pprint
from unittest import TestCase

from k8_vmware.helpers.View_Soap_Calls import View_Soap_Calls
from k8_vmware.vsphere.Firewall import Firewall


class test_Firewall(TestCase):

    def setUp(self) -> None:
        self.firewall = Firewall()

    def test_rules(self):
        with View_Soap_Calls():
            result = self.firewall.rules()

            import json
            pprint(result)