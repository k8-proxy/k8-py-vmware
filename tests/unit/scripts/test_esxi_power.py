import os
from pprint import pprint
from unittest import TestCase

from scripts.esxi_power import Esxi_Power
from scripts.utils import Utils


class test_VMUtils(TestCase):
    def setUp(self) -> None:
        os.environ["mode_tag"]          = "start"
        os.environ["auto"]              = "0"
        os.environ["start_shut_tag"]    = "ab-test-start"
        os.environ["not_shutdown_tag"]  = "ab-test-donot-shutdown"
        os.environ["scheduled_start"]   = "Wednesday,10:59AM"
        os.environ["scheduled_stop"]    = "Monday,9:30PM"
        self.esxi_power                 = Esxi_Power()

    def test__init__(self):
        assert self.esxi_power.mode_tag == os.environ["mode_tag"]

    def test_get_targets(self):
        targets = self.esxi_power.get_targets()
        assert len(targets) > 0

    def test_validate_scheduled_mode(self):
        expected_dt = self.esxi_power.validate_scheduled_mode()
        self.assertEqual(expected_dt, os.environ['scheduled_start'])

    def test_format_expected_date(self):
        expected_date = Utils.format_expected_date("Friday,10:30AM", "%Y-%m-%d %I:%M%p")
        self.assertTrue("10:30AM" in expected_date)
