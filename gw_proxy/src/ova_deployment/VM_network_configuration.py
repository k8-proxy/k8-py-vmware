import os
import atexit
import time
import ssl 
from pyVim import connect
from pyVmomi import vim, vmodl

# Disabling SSL certificate verification 
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1) 
context.verify_mode = ssl.CERT_NONE 

inputs = {'vcenter_ip': os.environ.get("VSPHERE_HOST"),
          'vcenter_password': os.environ.get('VSPHERE_PASSWORD'),
          'vcenter_user': os.environ.get('VSPHERE_USERNAME'),
          'vm_name' : os.environ.get('vm_name'),
          'isDHCP' : False,
          'vm_ip' : os.environ.get("VM_IP"),
          'subnet' : os.environ.get("VM_SUBNET"),
          'gateway' : os.environ.get("VM_GATEWAY"),
          'dns' : ['8.8.8.8'],
          'domain' : os.environ.get("VSPHERE_HOST")
          }


def get_obj(content, vimtype, name):
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj


def add_nic(vm, network):
    spec = vim.vm.ConfigSpec()

    # add Switch here
    dev_changes = []
    switch_spec                = vim.vm.device.VirtualDeviceSpec()
    switch_spec.operation      = vim.vm.device.VirtualDeviceSpec.Operation.add
    switch_spec.device         = vim.vm.device.VirtualVmxnet3()

    switch_spec.device.backing = vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
    switch_spec.device.backing.useAutoDetect = False
    switch_spec.device.backing.deviceName = network.name
    switch_spec.device.backing.network = network
    switch_spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
    switch_spec.device.connectable.startConnected = True
    switch_spec.device.connectable.connected = True

    dev_changes.append(switch_spec)

    spec.deviceChange = dev_changes
    output = vm.ReconfigVM_Task(spec=spec)
    time.sleep(2)
    print output.info


def wait_for_task(task, actionName='job', hideResult=False):
    """
    Waits and provides updates on a vSphere task
    """

    while task.info.state == vim.TaskInfo.State.running or task.info.state == vim.TaskInfo.State.queued:
        time.sleep(2)

    if task.info.state == vim.TaskInfo.State.success:
        if task.info.result is not None and not hideResult:
            out = '%s completed successfully, result: %s' % (actionName, task.info.result)
            print out
        else:
            out = '%s completed successfully.' % actionName
            print out
    else:
        out = '%s did not complete successfully: %s' % (actionName, task.info.error)
        print out
        raise task.info.error #error happens here

    return task.info.result


def ip_assign(vm):
    adaptermap = vim.vm.customization.AdapterMapping()
    globalip = vim.vm.customization.GlobalIPSettings()
    adaptermap.adapter = vim.vm.customization.IPSettings()

    """Static IP Configuration"""
    adaptermap.adapter.ip = vim.vm.customization.FixedIp()
    adaptermap.adapter.ip.ipAddress = inputs['vm_ip']
    adaptermap.adapter.subnetMask = inputs['subnet']
    adaptermap.adapter.gateway = inputs['gateway']  
    globalip.dnsServerList = inputs['dns']

    adaptermap.adapter.dnsDomain = inputs['domain']

    # Hostname settings
    ident = vim.vm.customization.LinuxPrep()
    ident.domain = inputs['domain']
    ident.hostName = vim.vm.customization.FixedName()
    ident.hostName.name = inputs['vm_name']

    customspec = vim.vm.customization.Specification()
    customspec.nicSettingMap = [adaptermap]
    customspec.globalIPSettings = globalip
    customspec.identity = ident

    print "Reconfiguring VM Networks . . ."
    task = vm.Customize(spec=customspec)

    # Wait for Network Reconfigure to complete
    wait_for_task(task, "config task") #error happens here



if __name__ == '__main__':
    service_instance = connect.SmartConnect(host=inputs['vcenter_ip'], user=inputs['vcenter_user'], pwd=inputs['vcenter_password'], sslContext=context)
    atexit.register(connect.Disconnect, service_instance)

    content = service_instance.RetrieveContent()
    vm = get_obj(content, [vim.VirtualMachine], inputs['vm_name'])
    network = get_obj(content, [vim.Network], "DMZ")

    add_nic(vm, network)
    ip_assign(vm)