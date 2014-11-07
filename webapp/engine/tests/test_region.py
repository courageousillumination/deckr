"""
Contains any tests around Regions.
"""

from unittest import TestCase

from engine.region import Region
from engine.zone import Zone


class GameRunnerTestCase(TestCase):

    """
    A simple test case for testing anything related to regions.
    """

    def test_get_add_zones(self):
        """
        Test ability to get list of zones. Also tests adding zones.
        """

        zone1 = Zone()
        zone2 = Zone()
        zone3 = Zone()
        region = Region()

        self.assertEqual(0, len(region.get_zones()))

        region.add_zone(zone1)
        region.add_zone(zone2)

        self.assertListEqual([zone1, zone2], region.get_zones())
        self.assertNotIn(zone3, region.get_zones())
