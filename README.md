# k8-vmware

[![Run Python Tests](https://github.com/k8-proxy/k8-vmware/workflows/Run%20Python%20Tests/badge.svg)](https://github.com/k8-proxy/k8-vmware/actions)


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