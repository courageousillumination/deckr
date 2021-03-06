"""
This module exports the HasZones mixin.
"""

from copy import copy

from engine.zone import Zone


class HasZones(object):

    """
    A class that inherits from this class has zones. This mixin exports
    the add_zones and add_zone features.
    """

    def __init__(self):
        super(HasZones, self).__init__()

        self.zones = {}

    def add_zones(self, zones):
        """
        Takes in a list of zone configs and adds them all in one go.
        Includes code for dealing with multiplicity.
        """

        for zone in zones:

            multiplicity = zone.get('multiplicity', None)
            if multiplicity is not None:
                base_name = zone['name']
                # We need to make a copy here since we mutate the name element
                # below.
                zone_copy = copy(zone)
                for i in range(multiplicity):
                    zone_copy['name'] = base_name + str(i)
                    self.add_zone(zone_copy)
            else:
                self.add_zone(zone)

    def add_zone(self, zone_config):
        """
        Takes in a single zone configuration and sets it up. This includes
        setting an attribute with that zone name and adding it to the zones
        dictionary.
        """

        zone_object = Zone(zone_config)
        self.zones[zone_object.name] = zone_object
        setattr(self, zone_object.name, zone_object)
