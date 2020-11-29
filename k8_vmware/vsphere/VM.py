class VM:
    def __init__(self, vm):
        self.vm = vm

    def config(self):
        return self.summary().config

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
