import ssl
import requests
from osbot_utils.utils.Files import temp_file

from k8_vmware.Config import Config
from k8_vmware.vsphere.Datastore import Datastore
from k8_vmware.vsphere.Sdk import Sdk


class Datastore_File:

    def __init__(self, ds_folder, ds_file):
        self.sdk = Sdk()
        self.datastore   = Datastore()
        self.config      = Config()
        self.ds_folder   = ds_folder
        self.ds_file     = ds_file
        self.verify_cert = False

    def get_headers(self):
        return {'Content-Type': 'application/octet-stream'}

    def get_host(self):
        return self.config.vsphere_host()

    def get_request_cookie(self):
        client_cookie = self.sdk.service_instance()._stub.cookie
        cookie_name   = client_cookie.split("=", 1)[0]
        cookie_value  = client_cookie.split("=", 1)[1].split(";", 1)[0]
        cookie_path   = client_cookie.split("=", 1)[1].split(";", 1)[1].split(";", 1)[0].lstrip()
        cookie_text   = " " + cookie_value + "; $" + cookie_path
        cookie = dict()
        cookie[cookie_name] = cookie_text
        return cookie

    def get_params(self):
        return {"dsName": self.datastore.name, "dcPath": self.datastore.datacenter}

    def get_remote_file(self):
        return f"{self.ds_folder}/{self.ds_file}"

    def get_server_url(self):
        host        = self.get_host()
        remote_file = self.get_remote_file()
        resource    = "/folder/" + remote_file
        return  "https://" + host + ":443" + resource

    def requests_download_from_url(self):
        tmp_file = temp_file()

        cookie      = self.get_request_cookie()
        headers     = self.get_headers()
        params      = self.get_params()
        server_url  = self.get_server_url()



        with open(tmp_file, "wb") as file:
            response = requests.get(server_url, params=params, headers=headers, cookies=cookie, verify=self.verify_cert)
            file.write(response.content)
        return tmp_file

    def download(self):
        return self.requests_download_from_url()

    def upload(self, path_file):
        remote_file = f"{self.ds_folder}/{self.ds_file}"
        return self.requests_upload_to_url(path_file, remote_file)