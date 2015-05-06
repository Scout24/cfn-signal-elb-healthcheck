from unittest import TestCase

import cseh
from mock import patch


class TestSignalElbHealthcheck(TestCase):

    @patch("cseh.get_instance_metadata")
    def test_get_region_strips_availability_zone_to_region(self, get_instance_metadata):
        get_instance_metadata.return_value = { "availability-zone": "eu-west-1b" }

        self.assertEqual(cseh.get_region(), "eu-west-1")