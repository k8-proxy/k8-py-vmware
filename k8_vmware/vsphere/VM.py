import pyVmomi


class VM:
    def __init__(self, vm):
        self.vm = vm

    def config(self):
        return self.summary().config

    def devices(self):
        return self.vm.config.hardware.device

    def devices_Virtual_IDE_Controller      (self): return self.devices_of_type(pyVmomi.vim.vm.device.VirtualIDEController     )
    def devices_Virtual_Cdrom               (self): return self.devices_of_type(pyVmomi.vim.vm.device.VirtualCdrom             )
    def devices_Virtual_AHCI_Controller     (self): return self.devices_of_type(pyVmomi.vim.vm.device.VirtualAHCIController    )
    def devices_Virtual_PCNet_32            (self): return self.devices_of_type(pyVmomi.vim.vm.device.VirtualPCNet32           )
    def devices_Virtual_Vmxnet_2            (self): return self.devices_of_type(pyVmomi.vim.vm.device.VirtualVmxnet2           )
    def devices_Virtual_Vmxnet_3            (self): return self.devices_of_type(pyVmomi.vim.vm.device.VirtualVmxnet3           )
    def devices_Virtual_E1000               (self): return self.devices_of_type(pyVmomi.vim.vm.device.VirtualE1000             )
    def devices_Virtual_E1000e              (self): return self.devices_of_type(pyVmomi.vim.vm.device.VirtualE1000e            )
    def devices_Virtual_Sriov_EthernetCard  (self): return self.devices_of_type(pyVmomi.vim.vm.device.VirtualSriovEthernetCard )

    def devices_of_type(self, type):
        devices = []
        for device in self.hardware().device:
            if isinstance(device, type):
                devices.append(device)
        return devices

    def devices_indexed_by_label(self):
        devices = {}
        for device in self.devices():
            key = device.deviceInfo.label
            value = device
            devices[key] = value
        return devices

    def guest(self):
        return self.summary().guest

    def info(self):
        summary = self.summary()                # need to do this since each reference to self.vm.summary.config is call REST call to the server
        #print(summary)
        config  = summary.config                # these values are retrieved on the initial call to self.vm.summary
        guest   = summary.guest                 # using self.vm.summary.guest here would had resulted in two more REST calls
        runtime = summary.runtime

        info = {
                    "Annotation"        : config.annotation      ,
                    "BootTime"          : str(runtime.bootTime)  ,
                    "ConnectionState"   : runtime.connectionState,
                    "GuestId"           : config.guestId         ,
                    "GuestFullName"     : config.guestFullName   ,
                    "Host"              : runtime.host           ,
                    "HostName"          : guest.hostName         ,
                    "IP"                : guest.ipAddress        ,
                    "MemorySizeMB"      : config.memorySizeMB    ,
                    "MOID"              : self.vm._moId          ,
                    "Name"              : config.name            ,
                    "MaxCpuUsage"       : runtime.maxCpuUsage    ,
                    "MaxMemoryUsage"    : runtime.maxMemoryUsage ,
                    "NumCpu"            : config.numCpu          ,
                    "PathName"          : config.vmPathName      ,
                    "StateState"        : runtime.powerState     ,
                    "Question"          : None                   ,
                    "UUID"              : config.uuid
            }
        # if guest            != None: info['IP']        = guest.ipAddress
        if runtime.question != None: info['Question']  = runtime.question.text,
        return info

    def hardware(self):
        return self.vm.config.hardware

    def host_name(self):
        return self.guest().hostName

    def ip(self):
        return self.guest().ipAddress

    def name(self):
        return self.config().name

    def moid(self):
        return self.vm._moId

    def powered_state(self):
        return self.runtime().powerState

    def powered_on(self):
        return self.powered_state() == 'poweredOn'

    def powered_off(self):
        return self.powered_state() == 'poweredOff'

    def summary(self):
        return self.vm.summary                              # will make REST call to RetrievePropertiesEx

    def task(self):
        from k8_vmware.vsphere.VM_Task import VM_Task       # have to do this import here due to circular dependencies (i.e. VM_Task imports VM)
        return VM_Task(self)

    def runtime(self):
        return self.vm.summary.runtime

    def uuid(self):
        return self.config().uuid

    def __str__(self):
        return f'[VM] {self.name()}'
