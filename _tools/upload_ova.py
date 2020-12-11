from k8_vmware.vsphere.OVA import OVA

ova_path = "/Users/diniscruz/Downloads/icap-ovas/2nd Dec/photon-uefi-hw13-4.0-d98e681.ova"

ova = OVA()
ova.upload_ova(ova_path)
