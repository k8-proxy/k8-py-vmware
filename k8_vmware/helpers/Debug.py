# Helper methods to be used during development
from os import environ

class Debug:

    def print_soap_calls(self):                    # use this to see SOAP calls made to the /sdk endpoint
        environ['show_soap_calls'] = "True"        # good to debug performance issues
        # here is the code added (locally) to line 1352 of the SoapAdapter.py file
        #   if environ.get('show_soap_calls'):
        #        print(f"[SoapAdapter (POST)] {info.wsdlName}")  # DC use this to see the calls made via the /SDK
