from unittest import TestCase, skip

from engine.region import Region
from engine.zone import Zone

class GameRunnerTestCase(TestCase):
    
    @skip("not yet implemented")
    def test_get_add_zones(self):
    	zone1 = Zone()
    	zone2 = Zone()
    	zone3 = Zone()

    	testregion = Region()
    	testregion.add_zone(zone1)
    	testregion.add_zone(zone2)

    	self.assertListEqual([zone1,zone2],testregion.get_zones())
    	self.assertNotIn(zone3,testregion.get_zones())