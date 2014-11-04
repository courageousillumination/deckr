from unittest import TestCase, skip

import engine.region

class GameRunnerTestCase(TestCase):
    
    def test_get_zones(self):
    	engine.region.zones.append(zone1)
    	engine.region.zones.append(zone2)
    	assertListEqual([zone1,zone2],engine.region.zones)