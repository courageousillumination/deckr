"""
This module provides the Region class.
"""

from engine.game_object import GameObject


class Region(GameObject):

    """
    A region is basically a collection of zones.
    """

    def __init__(self):
        super(Region, self).__init__()
        self.zones = []

    def add_zone(self, zone):
        """
        Add a zone to this region.
        """

        self.zones.append(zone)

    def get_zones(self):
        """
        Get all the zones out of this region.
        """

        return self.zones
