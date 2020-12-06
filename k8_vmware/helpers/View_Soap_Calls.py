
####### use this to see SOAP calls made to the /sdk endpoint #######

# good to debug performance issues

# todo refactor the rest of the code below into a before_call (the 1st part is done, what is needed now is the method handles the request
# This is the code added (locally) to line 1352 of the SoapAdapter.py file
#         from os import environ
#          if environ.get('show_soap_calls'):
#             print(f"[SOAP-CALL] {info.wsdlName:30} : {info.methodResultName}")             # DC use this to see the calls made via the /SDK
#
#          if environ.get('show_soap_calls_xml'):
#             req_xml = str(req.decode())
#             import xml.dom.minidom
#             dom = xml.dom.minidom.parseString(req_xml)
#             xml_string = dom.toprettyxml()
#             xml_string = os.linesep.join([f"\t{s}" for s in xml_string.splitlines() if s.strip()])  # remove the weird newline issue
#             xml_string = xml_string.replace(' xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"', "") \
#                                    .replace(' xmlns="urn:vim25"',"")
#             print(f"\n{xml_string}\n")

# class used like this
#   with View_Soap_Calls(show_xml=True):
#       ... code .....

from os import environ

from pyVmomi import SoapAdapter

from k8_vmware.helpers.for_osbot_utils.Wrap_Method import Wrap_Method

def before_call(*args, **kwargs):
    info = args[2]
    from os import environ
    if environ.get('show_soap_calls'):
        print(
            f"[SOAP-CALL] {info.wsdlName:30} : {info.methodResultName}")  # DC use this to see the calls made via the /SDK
    return (args, kwargs)

class View_Soap_Calls:

    def __init__(self, show_xml=False, show_calls=True):
        self.show_xml       = show_xml
        self.show_calls     = show_calls
        self.target_module  = SoapAdapter.SoapStubAdapter
        self.target_method  = "InvokeMethod"
        self.wrap_method    = None

    def __enter__(self):
        return self.start()

    def __exit__(self, type, value, traceback):
        self.stop()

    def start(self):
        self.wrap_target_method()
        if self.show_calls or self.show_xml:
            print()
            print("*******************************************************")
            print("***** Staring showing SOAP calls to /sdk endpoint *****")
            print("*******************************************************")
        if self.show_calls:
            environ['show_soap_calls'    ] = "True"
        if self.show_xml:
            environ['show_soap_calls_xml'] = "True"
        return self


    def stop(self):
        self.unwrap_target_method()
        if self.show_calls:
            del environ['show_soap_calls'    ]
        if self.show_xml:
            del environ['show_soap_calls_xml']
        if self.show_calls or self.show_xml:
            print("#######################################################")
            print("##### Stopped showing SOAP calls to /sdk endpoint #####")
            print("#######################################################")
            print()
        return self

    def wrap_target_method(self):
        self.wrap_method = Wrap_Method(self.target_module, self.target_method)
        self.wrap_method.add_on_before_call(before_call)
        self.wrap_method.wrap()

    def unwrap_target_method(self):
        self.wrap_method.unwrap()