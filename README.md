# k8-vmware

[![Run Python Tests](https://github.com/k8-proxy/k8-vmware/workflows/Run%20Python%20Tests/badge.svg)](https://github.com/k8-proxy/k8-vmware/actions)
[![Coverage Status](https://coveralls.io/repos/github/k8-proxy/k8-vmware/badge.svg?branch=main&kill_cache=1)](https://coveralls.io/github/k8-proxy/k8-vmware?branch=main)
[![Known Vulnerabilities](https://snyk.io/test/github/k8-proxy/k8-vmware/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/k8-proxy/k8-vmware?targetFile=requirements.txt)

API that simplifies the use of the [pyvmomi](https://github.com/vmware/pyvmomi) which is a python wrapper around the VMWare ESXi soap-based api (see [VMware vSphere API Reference Documentation](https://code.vmware.com/apis/968))

Other similar implementations and good sources of pyvmomi examples:
- [pyvmomi-community-samples](https://github.com/vmware/pyvmomi-community-samples)
- [pyvmomi-tools](https://github.com/vmware-archive/pyvmomi-tools)
- [Ansible](https://github.com/ansible-collections/community.vmware/blob/main/plugins/modules/vmware_guest.py])
- [vlab_inf_common](https://github.com/willnx/vlab_inf_common)
- [adles](https://www.programcreek.com/python/?code=GhostofGoes%2FADLES%2FADLES-master%2Fadles%2Fvsphere%2Fvsphere_class.py#)



## ESXI01 reset procedure
* **Note**: After reset, this command must be executed so that packer could build and push images.

```esxcli system settings advanced set -o /Net/GuestIPHack -i 1```

- [Reference](https://www.packer.io/docs/builders/vmware/iso)


## Dev machine install

To install dependencies run command

```pip3 install -r requirements.txt```


## run tests

Set Virtual environment

```source venv/bin/activate```

Install k8_vmware package (as editable)

```pip install -e .```

Configure the environment variables, by renaming the `.env.example` file top `.env` and set these values

```export VSPHERE_HOST={IP of ESXi server}
export VSPHERE_USERNAME={username}
export VSPHERE_PASSWORD={password}``` 


