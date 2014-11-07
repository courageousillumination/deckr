"""
This module provides the Region class.
"""


class Region(object):

    """
    A region is basically a collection of zones.
    """

    def __init__(self):
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
