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
        """
        Add an object to a zone. This is an unordered operation.
        """

        self.objects.append(obj)

    def remove(self, obj):
        """
        Remove a specified object from a zone. Fails silently if the
        object is not in the list.
        """

        try:
            self.objects.remove(obj)
        except ValueError:
            pass

    def __contains__(self, obj):
        """
        Check if a zone contains the specified object.
        """

        return obj in self.objects

    def __iter__(self):
        """
        Returns an iterable of the objects in this zone.
        """

        return iter(self.objects)

    def __len__(self):
        """
        Count the number of objects in this zone.
        """

        return len(self.objects)

class OrderedZone(Zone):

    def push(self, obj):
        """
        Push an object on to this zone. This is an ordered operation.
        """

        self.objects.append(obj)

    def pop(self):
        """
        Pop the top element of this zone. If no object exists return None.
        """

        try:
            return self.objects.pop()
        except IndexError:
            return None

    def insert(self, obj, index):
        """
        Insert an object into the zone at the specified index.
        """

        self.objects.insert(index, obj)

    def shuffle(self):
        """
        Shuffle an ordered zone. This will randomize the order of the objects
        in the zone.
        """
        
        import random

        random.shuffle(self.objects)
