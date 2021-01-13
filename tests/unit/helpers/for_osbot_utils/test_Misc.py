from unittest import TestCase

from k8_vmware.helpers.for_osbot_utils.Misc import random_password


class test_Misc(TestCase):
    def test_random_password(self):
        password = random_password(length=24, prefix="")
        assert len(password) == 24
