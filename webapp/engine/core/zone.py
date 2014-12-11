"""
This module provides the Zone and OrderedZone classes and various
utility functions for zones.
"""

from engine.core.game_object import GameObject
from engine.mixins.configurable import Configurable


def create_zone(config):
    """
    This will create a zone from a specified configuration. If
    the 'ordered' attribute is set to True an ordered zone will be created
    otherwise we will create an unordered zone.
    """

    is_ordered = config.get('ordered', None)
    if is_ordered == True:
        zone_object = OrderedZone()
    else:
        zone_object = Zone()
    zone_object.load_config(config)
    return zone_object


class Zone(GameObject, Configurable):

    """
    A zone represents any region in a game. For the most part zones
    wrap lists, but they provide some additional functionality such
    as nested containment.
    """

    def __init__(self):
        super(Zone, self).__init__()

        self.objects = []

    def add(self, obj):
        self.objects.append(obj)

    def remove(self, obj):
        self.objects.remove(obj)

    def __contains__(self, obj):
        return obj in self.objects

    def __iter__(self):
        return iter(self.objects)

    def __len__(self):
        return len(self.objects)

class OrderedZone(Zone):

    def push(self, obj):
        self.objects.append(obj)

    def pop(self):
        try:
            return self.objects.pop()
        except IndexError:
            return None

    def insert(self, obj, index):
        self.objects.insert(index, obj)

    def shuffle(self):
        import random

        random.shuffle(self.objects)
