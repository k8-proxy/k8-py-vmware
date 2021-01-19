from k8_vmware.helpers.TestCase_OVA import TestCase_OVA

class test_TestOVA_VM(TestCase_OVA):

    def test_setUpClass(self):
        assert type(self.vm_name   ) == str
        assert self.vm_name      is     not None
        assert self.url          is     not None
        assert self.ova_path     is     not None