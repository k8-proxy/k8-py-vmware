import pyVmomi
from osbot_utils.decorators.Lists import index_by, group_by

from k8_vmware.helpers.View_Soap_Calls import View_Soap_Calls
from k8_vmware.vsphere.Sdk import Sdk
from k8_vmware.vsphere.Task import Task


class Datastore:

    def __init__(self, name="datastore1"):
        self.name = name
        self.sdk  = Sdk()

    def datastore(self):
        return self.sdk.get_object(pyVmomi.vim.Datastore, self.name)

    def info(self):
        info = self.datastore().info
        vmfs = info.vmfs
        data = {
                    "Capacity": self.sizeof_fmt(vmfs.capacity)   ,
                    "Name"    : info.name       ,
                    "Type"    : vmfs.type       ,
                    "SSD"     : vmfs.ssd        ,
                    "UUID"    : vmfs.uuid       ,
               }
        return data

    def add_query_details_to_search_spec(self,search_spec):
        query_details       = pyVmomi.vim.host.DatastoreBrowser.FileInfo.Details(fileOwner    = True,
                                                                                 fileSize     = True,
                                                                                 fileType     = True,
                                                                                 modification = True)
        search_spec.details = query_details
        return self

    def execute_search_task(self, search_function, search_spec):
        self.add_query_details_to_search_spec(search_spec)
        task  = search_function("[%s]" % self.name, search_spec)
        Task().wait_for_task(task)
        return task.info.result

    def get_search_data__for_files(self, search_results):
        data = []
        for item in  search_results:
            #print(item)
            for file in item.file:
                data.append({
                                "Folder_path": item.folderPath               ,
                                "Modified"   : str(file.modification)        ,
                                "Owner"      : file.owner                    ,
                                "FileName"   : file.path                     ,
                                "Size"       : self.sizeof_fmt(file.fileSize),
                                "Type"       : type(file).__name__.replace('vim.host.DatastoreBrowser.','')
                             })
        return data

    def get_search_data__for_folders(self, search_results):
        data = []
        for item in  search_results:
            data.append({
                            "Modified"  : str(item.modification)        ,
                            "Owner"     : item.owner                    ,
                            "FolderName": item.path                     ,
                            "Size"      : self.sizeof_fmt(item.fileSize)
                         })
        return data

    @index_by
    @group_by
    def files(self, match_pattern="*"):
        search_function          = self.datastore().browser.SearchDatastoreSubFolders_Task
        search_spec              = pyVmomi.vim.HostDatastoreBrowserSearchSpec()
        search_spec.matchPattern = match_pattern
        search_results           = self.execute_search_task(search_function, search_spec)
        return self.get_search_data__for_files(search_results)

    def files_names(self, match_pattern="*"):
        return sorted(list(set(self.files(match_pattern, index_by='FileName'))))

    def files_paths(self, match_pattern="*"):
        files = self.files(match_pattern)
        paths = []
        for file in files:
            path = f"/{file['Folder_path']}/{file['FileName']}"
            path = path.replace(f'[{self.name}] ', "")          # remove datastore from path
            paths.append(path)

        return sorted(paths)

    # note the content.fileManager.MakeDirectory doesn't return a Task so need to keep an eye on this for side effect
    # it might be that these legacy methods do the folder creation in a sync way (vs a task)
    def folder_create(self, folder_name):
        folder_path = f'[{self.name}]/{folder_name}'
        content = self.sdk.content()
        datacenter = self.sdk.datacenter()
        content.fileManager.MakeDirectory(name=folder_path, datacenter=datacenter, createParentDirectories=True) # this method doesn't return a task
        #Task().wait_for_task(task)
        return True

    def folder_delete(self, folder_name):
        folder_path = f'[{self.name}]/{folder_name}'
        content    = self.sdk.content()
        datacenter = self.sdk.datacenter()
        try:
            task = content.fileManager.DeleteDatastoreFile_Task(folder_path, datacenter)
            Task().wait_for_task(task)
            if task.info.state == "success":
                return True
        except Exception as error:
            print(f"[Error][folder_delete] {error.msg}")  #todo: add global error handler and use it here
        return False


    @index_by
    @group_by
    def folders(self, match_pattern="*"):
        search_function = self.datastore().browser.SearchSubFolders

        query_folder    = pyVmomi.vim.host.DatastoreBrowser.FolderQuery()
        search_spec     = pyVmomi.vim.host.DatastoreBrowser.SearchSpec(query=[query_folder])
        search_spec.matchPattern = match_pattern
        search_results = self.execute_search_task(search_function, search_spec)
        return self.get_search_data__for_folders(search_results[0].file)

    def folders_names(self, match_pattern="*"):
        return sorted(list(set(self.folders(match_pattern, index_by="FolderName"))))

    def sizeof_fmt(self, num):
        """
        Returns the human readable version of a file size
        :param num:
        :return:
        """
        for item in ['bytes', 'KB', 'MB', 'GB']:
            if num < 1024.0:
                return "%3.1f %s" % (num, item)
            num /= 1024.0
        return "%3.1f %s" % (num, 'TB')