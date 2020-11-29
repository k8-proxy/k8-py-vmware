from unittest import TestCase

from k8_vmware.vsphere.VM_Create import VM_Create


class test_VM_Create(TestCase):
    def setUp(self) -> None:
        self.vm_create = VM_Create()

    def test__init__(self):
        assert 'random_name_' in self.vm_create.vm_name
        assert self.vm_create.data_store == 'datastore1'
        assert self.vm_create.guest_id   == 'ubuntu64Guest'

    def test_vm_create__delete(self):
        print()
        vm               = self.vm_create.create()
        assert vm.name() == self.vm_create.vm_name

        task_delete     = vm.task().delete()
        assert task_delete.info.state == "success"