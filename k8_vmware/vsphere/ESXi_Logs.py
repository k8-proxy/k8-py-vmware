from osbot_utils.utils.Files import file_contents, file_delete

from k8_vmware.vsphere.ESXi_Ssh import ESXi_Ssh


class ESXi_Logs:

    def __init__(self):
        self.esxi_ssh = ESXi_Ssh()

    def log_files(self):
        return self.esxi_ssh.ls('/var/log/*.log').split('\n')

    def get_log_file(self, log_file, size=0):
        path = f'/var/log/{log_file}.log'
        if size > 0:
            return self.esxi_ssh.tail(path, size)

        log_file = self.esxi_ssh.exec_scp_command(path)
        if log_file:
            log_data = file_contents(log_file)
            file_delete(log_file)
            return log_data

        #return self.esxi_ssh.cat(path)

    def auth         (self, size=0): return self.get_log_file('auth'         , size) # Authentication	                    /var/log/auth.log	            Contains all events related to authentication for the local system.
    def hostd        (self, size=0): return self.get_log_file('hostd'        , size) # ESXi host agent log	                /var/log/hostd.log	            Contains information about the agent that manages and configures the ESXi host and its virtual machines.
    def shell        (self, size=0): return self.get_log_file('shell'        , size) # Shell log	                        /var/log/shell.log	            Contains a record of all commands typed into the ESXi Shell and shell events (for example, when the shell was enabled).
    def syslog       (self, size=0): return self.get_log_file('syslog'       , size) # System messages	                    /var/log/syslog.log	            Contains all general log messages and can be used for troubleshooting. This information was formerly located in the messages log file.
    def vmauthd      (self, size=0): return self.get_log_file('vmauthd'      , size) # vMotion authentication daemon log	/var/log/vmauthd.log
    def vmkernel     (self, size=0): return self.get_log_file('vmkernel'     , size) # VMkernel	                            /var/log/vmkernel.log	        Records activities related to virtual machines and ESXi.
    def vmksummary   (self, size=0): return self.get_log_file('vmksummary'   , size) # VMkernel summary	                    /var/log/vmksummary.log	        Used to determine uptime and availability statistics for ESXi (comma separated).
    def vmkwarning   (self, size=0): return self.get_log_file('vmkwarning'   , size) # VMkernel warnings	                /var/log/vmkwarning.log	        Records activities related to virtual machines.
    def vobd         (self, size=0): return self.get_log_file('vobd'         , size) # VMware observer daemon log	        /var/log/vobd.log
    def vpxa         (self, size=0): return self.get_log_file('vpxa'         , size) # vCenter Server agent log	            /var/log/vpxa.log	            Contains information about the agent that communicates with vCenter Server (if the host is managed by vCenter Server).

