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

    def serialize(self, full=True):
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
                result[key] = self.process_for_serialize(getattr(self, key),
                                                         full)
        return result

    ################################################
    # Code to ensure attribute changes are tracked #
    ################################################

    def __setattr__(self, name, value):

        super(GameObject, self).__setattr__(name, value)

        # This is ugly but gets around that this will be called when we set game
        # in __init__
        if not hasattr(self, 'game'):
            return

        if self.game is not None and name in self.game_attributes:
            self.game.add_transition(None)
