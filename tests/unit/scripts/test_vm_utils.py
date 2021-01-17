import os
from pprint import pprint
from unittest import TestCase

from scripts.vm_utils import VMUtils


class test_VMUtils(TestCase):
    def setUp(self) -> None:
        self.vm_utils = VMUtils()

    def test__init__(self):
        pass
        # assert self.vm_utils.mode_tag == os.environ["mode_tag"]

    def test_get_targets(self):
        targets = self.vm_utils.get_targets()
        assert len(targets) > 0

    def test_do_actions(self):
        # To Do
        pass

    def test_validate_scheduled_mode(self):
        # To Do
        pass

    def test_format_expected_date(self):
        # To Do
        pass
