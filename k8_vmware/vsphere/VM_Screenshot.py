from osbot_utils.utils.Files import file_copy

from k8_vmware.vsphere.Datastore_File import Datastore_File
from k8_vmware.vsphere.Task import Task


class VM_Screenshot:
    def __init__(self, vm, target_file=None, ds_delete_on_download=True):
        self.vm                    = vm
        self.path_screenshot       = target_file
        self.ds_screenshot         = None
        self.ds_delete_on_download = ds_delete_on_download
        return vm

    def __enter__(self, target_file = '/tmp/vm_screeshot.png'):
        self.path_screenshot = target_file

    def __exit__(self, type, value, traceback):
        self.download()

    def download(self):
        self.save_screnshot_to_datastore()
        return self.download_screenshot_from_datastore()

    def download_screenshot_from_datastore(self):
        datastore_file = Datastore_File().set_file_from_path_datastore(self.ds_screenshot)
        local_temp_file = datastore_file.download()
        if (self.path_screenshot):
            file_copy(local_temp_file, self.path_screenshot)
        else:
            self.path_screenshot = local_temp_file
        if self.ds_delete_on_download:
            datastore_file.delete()
        return self.path_screenshot

    def save_screnshot_to_datastore(self):
        task = self.vm.vm.CreateScreenshot_Task()
        Task().wait_for_task(task)
        self.ds_screenshot = task.info.result
        return self.ds_screenshot