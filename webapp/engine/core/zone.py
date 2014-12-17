"""
This module provides the Zone and OrderedZone classes and various
utility functions for zones.
"""

from engine.core.game_object import GameObject
from engine.mixins.configurable import Configurable


class Zone(GameObject, Configurable):

    """
    A zone represents any region in a game. For the most part zones
    wrap lists, but they provide some additional functionality such
    as nested containment. Note that zones expose both unordered and ordered
    functionality; it is advised that you don't mix these.
    """

    def __init__(self):
        super(Zone, self).__init__()

        self.game_object_type = 'Zone'
        self.game_attributes.add('name')
        self.game_attributes.add('owner')

        self.objects = []

    def add_transition(self, transition_type, obj):
        """
        Add a transition whenever an object is added or removed from this zone.
        """

        if self.game is not None:
            self.game.add_transition({'name': transition_type,
                                      'object': obj.game_id,
                                      'zone': self.game_id})

    def add(self, obj):
        """
        Add an object to a zone. This is an unordered operation.
        """

        self.objects.append(obj)
        self.add_transition('add', obj)
        obj.zone = self

    def remove(self, obj):
        """
        Remove a specified object from a zone. Fails silently if the
        object is not in the list.
        """

        try:
            self.objects.remove(obj)
            self.add_transition('remove', obj)
        except ValueError:
            pass

    ######################
    # Ordered Operations #
    ######################

    def push(self, obj):
        """
        Push an object on to this zone. This is an ordered operation.
        """

        self.objects.append(obj)
        self.add_transition('add', obj)
        obj.zone = self

    def push_all(self, objs):
        """
        Push an iterable of objects on to this zone.
        """

        for obj in objs:
            self.push(obj)

    def pop(self):
        """
        Pop the top element of this zone. If no object exists return None.
        """

        try:
            obj = self.objects.pop()
            self.add_transition('remove', obj)
            return obj
        except IndexError:
            return None

    def pop_all(self):
        """
        Returns an ordered list of all items in this zone. They have now been
        removed.
        """

        result = []
        obj = self.pop()
        while obj != None:
            result.append(obj)
            obj = self.pop()
        return result

    def insert(self, obj, index):
        """
        Insert an object into the zone at the specified index.
        """

        self.objects.insert(index, obj)
        self.add_transition('add', obj)

    def shuffle(self):
        """
        Shuffle an ordered zone. This will randomize the order of the objects
        in the zone.
        """

        import random

        random.shuffle(self.objects)

    def serialize(self, player_id, full = True):
        """
        We override serialize because we only want to include ids in the objs
        and don't always want to track it's changes.
        """

        result = super(Zone, self).serialize(player_id, full)
        result['objects'] = [x.game_id for x in self.objects]
        return result


    #######################
    # Iterable operations #
    #######################

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

    def __getitem__(self, index):
        """
        Make sure we can use get item on a zone.
        """

        try:
            return self.objects[index]
        except IndexError:
            return None
