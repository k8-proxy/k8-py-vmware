from k8-vmware.k8_vmware.vsphere.OVA import *

# main
#!/usr/bin/env python
"""
Written by Nathan Prziborowski
Github: https://github.com/prziborowski

This code is released under the terms of the Apache 2
http://www.apache.org/licenses/LICENSE-2.0.html

Deploy an ova file either from a local path or a URL.
Most of the functionality is similar to ovf except that
that an OVA file is a "tarball" so tarfile module is leveraged.

"""
import atexit
import os
import os.path
import ssl
import sys
import time

from argparse import ArgumentParser
from getpass import getpass

from .tools import cli

from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim, vmodl

from .ovf_handler import OvfHandler


def setup_args():
    parser = cli.build_arg_parser()
    parser.add_argument('--ova-path',
                        help='Path to the OVA file, can be local or a URL.')
    parser.add_argument('--vm-name',
                        help='VM name to be created.')
    parser.add_argument('-d', '--datacenter',
                        help='Name of datacenter to search on. '
                             'Defaults to first.')
    parser.add_argument('-r', '--resource-pool',
                        help='Name of resource pool to use. '
                             'Defaults to largest memory free.')
    parser.add_argument('-ds', '--datastore',
                        help='Name of datastore to use. '
                             'Defaults to largest free space in datacenter.')
    return cli.prompt_for_password(parser.parse_args())

def get_dc(si, name):
    """
    Get a datacenter by its name.
    """
    for dc in si.content.rootFolder.childEntity:
        if dc.name == name:
            return dc
    raise Exception('Failed to find datacenter named %s' % name)


def get_rp(si, dc, name):
    """
    Get a resource pool in the datacenter by its names.
    """
    viewManager = si.content.viewManager
    containerView = viewManager.CreateContainerView(dc, [vim.ResourcePool],
                                                    True)
    try:
        for rp in containerView.view:
            if rp.name == name:
                return rp
    finally:
        containerView.Destroy()
    raise Exception("Failed to find resource pool %s in datacenter %s" %
                    (name, dc.name))


def get_largest_free_rp(si, dc):
    """
    Get the resource pool with the largest unreserved memory for VMs.
    """
    viewManager = si.content.viewManager
    containerView = viewManager.CreateContainerView(dc, [vim.ResourcePool],
                                                    True)
    largestRp = None
    unreservedForVm = 0
    try:
        for rp in containerView.view:
            if rp.runtime.memory.unreservedForVm > unreservedForVm:
                largestRp = rp
                unreservedForVm = rp.runtime.memory.unreservedForVm
    finally:
        containerView.Destroy()
    if largestRp is None:
        raise Exception("Failed to find a resource pool in dc %s" % dc.name)
    return largestRp

def get_ds(dc, name):
    """
    Pick a datastore by its name.
    """
    for ds in dc.datastore:
        try:
            if ds.name == name:
                return ds
        except:  # Ignore datastores that have issues
            pass
    raise Exception("Failed to find %s on datacenter %s" % (name, dc.name))


def get_largest_free_ds(dc):
    """
    Pick the datastore that is accessible with the largest free space.
    """
    largest = None
    largestFree = 0
    for ds in dc.datastore:
        try:
            freeSpace = ds.summary.freeSpace
            if freeSpace > largestFree and ds.summary.accessible:
                largestFree = freeSpace
                largest = ds
        except:  # Ignore datastores that have issues
            pass
    if largest is None:
        raise Exception('Failed to find any free datastores on %s' % dc.name)
    return largest


def main():
    args = setup_args()
    print(args.host, args.user, args.password, args.port)
    try:
        si = SmartConnectNoSSL(host=args.host,
                               user=args.user,
                               pwd=args.password,
                               port=args.port)
        atexit.register(Disconnect, si)
        print("connected successfully to esxi server %s!" % args.host)
    except:
        print("Unable to connect to %s" % args.host)
        return 1

    if args.vm_name:
        vm_name = args.vm_name
    else:
        vm_name = ""

    if args.datacenter:
        dc = get_dc(si, args.datacenter)
    else:
        dc = si.content.rootFolder.childEntity[0]

    if args.resource_pool:
        rp = get_rp(si, dc, args.resource_pool)
    else:
        rp = get_largest_free_rp(si, dc)

    if args.datastore:
        ds = get_ds(dc, args.datastore)
    else:
        ds = get_largest_free_ds(dc)

    ovf_handle = OvfHandler(args.ova_path)

    ovfManager = si.content.ovfManager
    # CreateImportSpecParams can specify many useful things such as
    # diskProvisioning (thin/thick/sparse/etc)
    # networkMapping (to map to networks)
    # propertyMapping (descriptor specific properties)
    cisp = vim.OvfManager.CreateImportSpecParams(entityName=vm_name)
    cisr = ovfManager.CreateImportSpec(ovf_handle.get_descriptor(),
                                       rp, ds, cisp)

    # These errors might be handleable by supporting the parameters in
    # CreateImportSpecParams
    if len(cisr.error):
        print("The following errors will prevent import of this OVA:")
        for error in cisr.error:
            print("%s" % error)
        return 1

    ovf_handle.set_spec(cisr)

    lease = rp.ImportVApp(cisr.importSpec, dc.vmFolder)
    while lease.state == vim.HttpNfcLease.State.initializing:
        print("Waiting for lease to be ready...")
        time.sleep(1)

    if lease.state == vim.HttpNfcLease.State.error:
        print("Lease error: %s" % lease.error)
        return 1
    if lease.state == vim.HttpNfcLease.State.done:
        return 0

    print("Starting deploy...")
    return ovf_handle.upload_disks(lease, args.host)


if __name__ == "__main__":
    exit(main())