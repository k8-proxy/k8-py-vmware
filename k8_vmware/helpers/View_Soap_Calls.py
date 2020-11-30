
####### use this to see SOAP calls made to the /sdk endpoint #######

# good to debug performance issues
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


class View_Soap_Calls:

    def __init__(self, show_xml=False, show_calls=True):
        self.show_xml   = show_xml
        self.show_calls = show_calls

    def __enter__(self):
        return self.start()

    def __exit__(self, type, value, traceback):
        self.stop()

    def start(self):
        if self.show_calls or self.show_xml:
            print()
            print("*******************************************************")
            print("***** Staring showing SOAP calls to /sdk endpoint *****")
            print("*******************************************************")
        if self.show_calls:
            environ['show_soap_calls'    ] = "True"
        if self.show_xml:
            environ['show_soap_calls_xml'] = "True"


    def stop(self):
        if self.show_calls:
            del environ['show_soap_calls'    ]
        if self.show_xml:
            del environ['show_soap_calls_xml']
        if self.show_calls or self.show_xml:
            print("#######################################################")
            print("##### Stopped showing SOAP calls to /sdk endpoint #####")
            print("#######################################################")
            print()
