"""
Contains any tests around the HasZones mixin
"""

from unittest import TestCase

from engine.core.zone import Zone
from engine.mixins.has_zones import HasZones


class MockHasZones(HasZones):
    def __init__(self):
        super(MockHasZones, self).__init__()
        self.zones_added = []

    def add_zone_callback(self, new_zone):
        self.zones_added.append(new_zone.name)

class HasZonesTestCase(TestCase):

    def setUp(self):
        self.has_zones = MockHasZones()

    def test_add_zone_simple(self):
        """
        Make sure we can create a simple zone.
        """

        self.has_zones.add_zone({'name': 'test_zone',
                                 'foo': 'bar'})
        self.assertTrue(isinstance(self.has_zones.test_zone, Zone))
        self.assertEqual(self.has_zones.test_zone.foo, 'bar')

    def test_add_zone_multiple(self):
        """
        See if the multiplicity keyword works to add multiple zones.
        """

        self.has_zones.add_zone({'name': 'test_zone', 'multiplicity': 2})

        self.assertTrue(isinstance(self.has_zones.test_zone0, Zone))
        self.assertTrue(isinstance(self.has_zones.test_zone1, Zone))

    def test_add_zones(self):
        """
        Make sure we can handle a list of zones.
        """

        self.has_zones.add_zones([{'name': 'test_zone1'},
                                  {'name': 'test_zone2'}])

        self.assertTrue(isinstance(self.has_zones.test_zone1, Zone))
        self.assertTrue(isinstance(self.has_zones.test_zone2, Zone))

    def test_add_zone_callback(self):
        """
        Make sure we call the add_zone callback in various circumstances.
        """

        self.has_zones.add_zone({'name': 'test_zone'})

        self.assertEqual(len(self.has_zones.zones_added), 1)
        self.assertIn('test_zone', self.has_zones.zones_added)
