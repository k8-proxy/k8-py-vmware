from unittest import TestCase

from osbot_utils.utils.Files import file_contents, temp_file
from osbot_utils.utils.Misc import random_string

from k8_vmware.vsphere.Datastore_File import Datastore_File


class test_Datastore_File(TestCase):

    def setUp(self) -> None:
        ds_folder           = ''
        ds_file             = 'new-one.txt'
        self.datastore_file = Datastore_File(ds_folder=ds_folder, ds_file=ds_file)

    def test_download(self):
        tmp_file = self.datastore_file.download()
        print(file_contents(tmp_file))

    def test_upload(self):
        path_file = temp_file(file_contents="This is a local file - " + random_string())
        result = self.datastore_file.upload(path_file)
        print(result)

    # def test_upload_file(self):
    #     ds_folder = ''
    #     ds_file   = 'new-one.txt'
    #     target_file = temp_file(".txt")
    #     self.datata
    #
    #
    # def __test_upload_file(self):
    #     sdk = self.datastore.sdk
    #     datacenter = sdk.datacenter()
    #
    #     host = Config().vsphere_server_details()['host']
    #     #remote_file='aaa.txt'
    #     remote_file = 'new-one.txt'
    #     resource = "/folder/" + remote_file
    #     params = {"dsName": self.datastore.name, "dcPath": datacenter.name}
    #
    #     http_url = "https://" + host + ":443" + resource
    #     def get_cookie_as_header():
    #         client_cookie = sdk.service_instance()._stub.cookie
    #         cookie_name = client_cookie.split("=", 1)[0]
    #         cookie_value = client_cookie.split("=", 1)[1].split(";", 1)[0]
    #         cookie_path = client_cookie.split("=", 1)[1].split(";", 1)[1].split(";", 1)[0].lstrip()
    #         cookie_text = " " + cookie_value + "; $" + cookie_path
    #         cookie = dict()
    #         cookie[cookie_name] = cookie_text
    #         return cookie
    #
    #     cookie = get_cookie_as_header()
    #     path_file = temp_file(file_contents="This is a local file")
    #     pprint(params)
    #     pprint(http_url)
    #
    #     headers = {'Content-Type': 'application/octet-stream'}
    #
    #     import ssl
    #     import requests
    #
    #     sslContext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    #     sslContext.verify_mode = ssl.CERT_NONE
    #
    #     verify_cert = False
    #
    #     print("download file: " + http_url)
    #     tmp_file = temp_file(extension='new_file.txt')
    #     with open(tmp_file, "wb") as f:
    #     # Connect and upload the file
    #         response = requests.get(http_url, params=params, headers=headers, cookies=cookie, verify=verify_cert)
    #         f.write(response.content)
    #         print(response.status_code)
    #
    #     print(f'file {tmp_file}')
    #     print(file_contents(tmp_file))
    #
    #
    #
    #     # # upload file
    #     # with open(path_file, "rb") as f:
    #     #     # Connect and upload the file
    #     #
    #     #     request = requests.put(http_url,
    #     #                            params=params,
    #     #                            data=f,
    #     #                            headers=headers,
    #     #                            cookies=cookie,
    #     #                            verify=verify_cert)
    #     #     print(request)
    #     #     print(request.text)
