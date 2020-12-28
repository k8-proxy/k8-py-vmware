from k8_vmware.Config import Config
from k8_vmware.vsphere.Sdk import Sdk


class Sdk_User:
    """
    Use this helper class to run commands user a particular user

    Restoring the default values in Config().vsphere_server_details() (into the Environment variables used)
    """

    def __init__(self, host=None, user_id=None, password=None):
        self.config             = None
        self.host               = host
        self.user_id            = user_id
        self.password           = password
        self.original_user_id   = ""
        self.original_password  = ""
        self.login_result       = None
        self.sdk                = Sdk()

    def __enter__(self):
        self.config            = Config()                                                               # get config object
        server_details         = self.config.vsphere_server_details()                                   # get server details (from env variables)
        self.original_username = server_details['username']                                             # store original values
        self.original_password = server_details['password']
        self.login_result      = self.sdk.login(host=self.host, user_id=self.user_id, password=self.password)    # relogin and force reload of SDK object
        return self

    def __exit__(self, ex_type, ex_value, ex_traceback):
        self.config.vsphere_set_server_details(username=self.original_username,
                                               password=self.original_password)                         # reset the server details to the original values
        self.login_result = self.sdk.login(force_reload=True)                                               # force reload of SDK object