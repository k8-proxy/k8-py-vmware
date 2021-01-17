# scripts

## vm_utils.py :
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
