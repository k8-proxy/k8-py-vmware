from os import environ
from unittest import TestCase

from k8_vmware.helpers.View_Soap_Calls import View_Soap_Calls


class test_View_Soap_Calls(TestCase):

    def setUp(self) -> None:
        self.view_soap_calls = View_Soap_Calls()

    def test__init__(self):
        assert self.view_soap_calls.show_xml      is False
        assert self.view_soap_calls.show_calls    is True
        assert environ.get('show_soap_calls'    ) is None
        assert environ.get('show_soap_calls_xml') is None

    def test___enter____exit__(self):
        assert environ.get('show_soap_calls'    ) is None
        assert environ.get('show_soap_calls_xml') is None

        with self.view_soap_calls:
            assert environ.get('show_soap_calls'    ) == "True"
            assert environ.get('show_soap_calls_xml') is None

        assert environ.get('show_soap_calls'    ) is None
        assert environ.get('show_soap_calls_xml') is None

    def test_start(self):                                       #todo add tests that capture the print statements and confirm what was printed. Do this via mocking of print method
        self.view_soap_calls.start()
        assert environ.get('show_soap_calls'    ) == "True"
        assert environ.get('show_soap_calls_xml') is None

        self.view_soap_calls.show_xml = True

        self.view_soap_calls.start()
        assert environ.get('show_soap_calls'    ) == "True"
        assert environ.get('show_soap_calls_xml') == "True"

        self.view_soap_calls.show_xml = True
        self.view_soap_calls.show_xml = True

        self.view_soap_calls.stop()
        assert environ.get('show_soap_calls'    ) is None
        assert environ.get('show_soap_calls_xml') is None

    def test_stop(self):
        self.view_soap_calls.show_xml = True

        self.view_soap_calls.start().stop()
        assert environ.get('show_soap_calls'    ) is None
        assert environ.get('show_soap_calls_xml') is None




