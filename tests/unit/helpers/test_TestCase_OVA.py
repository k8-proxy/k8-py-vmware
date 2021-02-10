from k8_vmware.helpers.TestCase_OVA import TestCase_OVA

class test_TestOVA_VM(TestCase_OVA):

    def test_setUpClass(self):
        assert self.ova_path is not None
        assert type(self.vm_name   ) == str
        assert self.url is not None
        assert self.vm_name      is     not None
