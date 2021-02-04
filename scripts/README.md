# scripts

## esxi_power.py :
- Contains method to start or stop VM based on input conditions.

- Required environment variables:
```
    VSPHERE_HOST=
    VSPHERE_USERNAME=
    VSPHERE_PASSWORD=
    mode_tag=start|shutdown
    auto=0|1
    start_shut_tag=
    not_shutdown_tag=
    scheduled_start=Wednesday,10:59AM
    scheduled_stop=Monday,9:30PM
```



## esxi_cleanup.py :

-  This script deletes VMs that it's age exceeds the number of expire days defined in environment variable **ESXI_EXPIRE_DAYS** except for the VMs with note that include **DONT_DELETE_NOTE** variable, Also will delete any VM with note that matches the environment variable **DELETE_NOTE** 
- Required environment variables:

```tex
 	VSPHERE_HOST=
 	VSPHERE_USERNAME=
 	VSPHERE_PASSWORD=
 	DELETE_NOTE=
 	DONT_DELETE_NOTE=
 	ESXI_EXPIRE_DAYS
```