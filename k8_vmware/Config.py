from os import environ
from dotenv import load_dotenv

class Config():
    def __init__(self):
        load_dotenv()

    def vsphere_server_details(self):
        return {
                    "host"    : environ.get('VSPHERE_HOST'),
                    "username": environ.get('VSPHERE_USERNAME'),
                    "password": environ.get('VSPHERE_PASSWORD')
                }