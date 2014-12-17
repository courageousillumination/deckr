"""
This module defines the GameObject.
"""


class GameObject(object):

    """
    A GameObject is any object in the game. A game object must have a type
    and an ID. Additionally one can specify attributes that should be tracked
    and transmitted about the game object.
    """

    def __init__(self):
        super(GameObject, self).__init__()
        # This is the ID of **this** object in the game.
        self.game_id = None
        # This specifies what type of object this is. This can be more
        # expressive than a simple class could be.
        self.game_object_type = None
        # game_attributes should be a set of all attributes that we care
        # about including in the state.
        self.game_attributes = set(['game_id', 'game_object_type'])

        # This is the actual game object that this belongs to.
        # NOTE: This has to be the last attribute set in __init__. After this
        # is set the __setattr__ will start checking all attributes.
        self.game = None

        # Any game object can be placed in a zone. When it is this will point
        # to it's zone. Don't make this a game attribute or there could be
        # significant trouble (infinite loops possibly). Note that it is the
        # Zone's responsibility to set this. It may not be entirely accurate,
        # since a Zone only updates on adds, not removes.
        self.zone = None

        self.player_overrides = {}

    ######################
    # Serialization code #
    ######################
    def serialize_single(self, obj, full):
        """
        This will serialize a single game object, either by grabbing
        just the game_id and game_object_type or by deffering to the serialize
        method on that object.
        """

        if not isinstance(obj, GameObject):
            return obj

        if not full:
            return {'game_id': obj.game_id,
                    'game_object_type': obj.game_object_type}
        else:
            return obj.serialize(True)

    def process_for_serialize(self, obj, full):
        """
        This function will process and object for serialization. It deals
        with three seperate cases.

        1) The object is a game object.
        2) A list of game objects
        3) A dictionary where values are game objects.
        """

        if isinstance(obj, list):
            return [self.serialize_single(x, full) for x in obj]
        elif isinstance(obj, dict):
            return {key: self.serialize_single(value, full) for
                    key, value in obj.items()}
        else:
            return self.serialize_single(obj, full)

    def serialize(self, player_id, full=True):
        """
        This will serialize this object for consumption by the outside
        world. This will basically construct a dictionary that contains
        the game_id, game_object_type and any other game_attributes. Can
        optionally specify full if one wants to recursivly include all sub
        game objects. If full is False then it will only include the game id
        and game_object_type of subobjects.
        """

        result = {}
        for key in self.game_attributes:
            if hasattr(self, key):
                value = self.get_value_for_player_id(key, player_id)
                result[key] = self.process_for_serialize(value, full)
        return result

    ################################################
    # Code to ensure attribute changes are tracked #
    ################################################

    def get_value_for_player_id(self, name, player_id):
        """
        Gets a value for a specific player. If an override is present, uses
        the override. Otherwise it falls back on any default attributes. If no
        default attribute is present it returns None.
        """
        if (player_id is not None and
                (name, player_id) in self.player_overrides):
            return self.player_overrides[(name, player_id)]

        if hasattr(self, name):
            return getattr(self, name)
        return None

    def set_player_override(self, name, value, player):
        """
        Sets the override for a specific player.
        """

        self.player_overrides[(name, player.game_id)] = value
        self.add_changed_value_transition(name, value, player.game_id)

    def add_changed_value_transition(self, name, value, player_id=None):
        """
        Whenever we change a value we may want to track it. If we do this
        function will add a transition on our game.
        """

        # This is ugly but gets around that this will be called when we set game
        # in __init__
        if not hasattr(self, 'game'):
            return

        if self.game is not None and name in self.game_attributes:
            self.game.add_transition({'name': 'set',
                                      'class': self.game_object_type,
                                      'game_id': self.game_id,
                                      'attribute': name,
                                      'value': value}, player_id=player_id)

    def __setattr__(self, name, value):
        super(GameObject, self).__setattr__(name, value)
        self.add_changed_value_transition(name, value)
