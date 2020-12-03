# k8-vmware

[![Run Python Tests](https://github.com/k8-proxy/k8-vmware/workflows/Run%20Python%20Tests/badge.svg)](https://github.com/k8-proxy/k8-vmware/actions)

API that simplifies the use of the [pyvmomi](https://github.com/vmware/pyvmomi) which is a python wrapper around the VMWare ESXi soap-based api (see [VMware vSphere API Reference Documentation](https://code.vmware.com/apis/968))

Other similar implementations and good sources of pyvmomi examples:
- [pyvmomi-community-samples](https://github.com/vmware/pyvmomi-community-samples)
- [pyvmomi-tools](https://github.com/vmware-archive/pyvmomi-tools)
- [Ansible](https://github.com/ansible-collections/community.vmware/blob/main/plugins/modules/vmware_guest.py])
- [vlab_inf_common](https://github.com/willnx/vlab_inf_common)
- [adles](https://www.programcreek.com/python/?code=GhostofGoes%2FADLES%2FADLES-master%2Fadles%2Fvsphere%2Fvsphere_class.py#)




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
