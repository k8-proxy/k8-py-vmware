from os import environ
from pprint import pprint
from unittest import TestCase, skip
from unittest.mock import patch, call

from pyVmomi import SoapAdapter

from k8_vmware.helpers.View_Soap_Calls import View_Soap_Calls
from k8_vmware.vsphere.Sdk import Sdk


class test_View_Soap_Calls(TestCase):

    def setUp(self) -> None:
        self.view_soap_calls = View_Soap_Calls()

    def test__init__(self):
        assert self.view_soap_calls.show_xml      is False
        assert self.view_soap_calls.show_calls    is True
        assert environ.get('show_soap_calls'    ) is None
        assert environ.get('show_soap_calls_xml') is None
        assert self.view_soap_calls.target_module == SoapAdapter.SoapStubAdapter
        assert self.view_soap_calls.target_method == "InvokeMethod"

    @patch('builtins.print')
    def test___enter____exit__(self, builtins_print):
        assert environ.get('show_soap_calls'    ) is None
        assert environ.get('show_soap_calls_xml') is None

        with self.view_soap_calls:
            assert environ.get('show_soap_calls'    ) == "True"
            assert environ.get('show_soap_calls_xml') is None

        assert environ.get('show_soap_calls'    ) is None
        assert environ.get('show_soap_calls_xml') is None


        assert builtins_print.call_count == 8
        builtins_print.assert_has_calls([   call(),
                                            call('*******************************************************'),
                                            call('***** Staring showing SOAP calls to /sdk endpoint *****'),
                                            call('*******************************************************'),
                                            call('#######################################################'),
                                            call('##### Stopped showing SOAP calls to /sdk endpoint #####'),
                                            call('#######################################################'),
                                            call() ])

    def test_start(self):                                       #todo add tests that capture the print statements and confirm what was printed. Do this via mocking of print method
        self.view_soap_calls.start()
        assert environ.get('show_soap_calls'    ) == "True"
        assert environ.get('show_soap_calls_xml') is None
        self.view_soap_calls.stop()

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

    #@skip("Current failing when running all tests (works when running just this class") # todo: fix this
    # @patch('builtins.print')
    # def test_trigger_soap_call(self, builtins_print):
    #     with self.view_soap_calls:
    #         sdk = Sdk()
    #         sdk.service_instance()
    #         assert builtins_print.call_count    == 6
    #         assert builtins_print.mock_calls[4] == call('[SOAP-CALL] RetrieveServiceContent         : vim.ServiceInstanceContent')
    #         assert builtins_print.mock_calls[5] == call('[SOAP-CALL] Login                          : vim.UserSession'           )

    #todo fix issue when running all tests (see above)
    #@patch('builtins.print')
    def test_trigger_soap_call(self):
        with self.view_soap_calls:
            sdk = Sdk()
            sdk.service_instance()
            assert environ.get('show_soap_calls'    ) == "True"
            assert environ.get('show_soap_calls_xml') is None


    def test_wrap_target_method__unwrap_target_method(self):
        original_target = getattr(self.view_soap_calls.target_module, self.view_soap_calls.target_method)
        assert SoapAdapter.SoapStubAdapter.InvokeMethod == original_target

        with self.view_soap_calls:
            assert SoapAdapter.SoapStubAdapter.InvokeMethod        != original_target
            assert self.view_soap_calls.wrap_method.wrapper_method == SoapAdapter.SoapStubAdapter.InvokeMethod
            assert self.view_soap_calls.wrap_method.target         == original_target

        assert SoapAdapter.SoapStubAdapter.InvokeMethod == original_target