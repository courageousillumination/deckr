"""
This module defines the StatefulGameObject.
"""

from engine.game_object import GameObject


class StatefulGameObject(GameObject):

    """
    A StatefulGameObject is any object in the game that
    has a state that we care about. Most GameObjects should probably
    be StatefulGameObjects. If we set the an attribute on a SGO then
    a transition is automtically created in the game that contains this
    SGO (note that this only applies if the attribute name is in
    game_attributes).
    """

    def __init__(self):
        super(StatefulGameObject, self).__init__()

        # What attributes shouldn't be tracked (internal attributes mainly)

        #self.no_track_attributes = set()
        #self.no_track_attributes.add("game_object_type")
        #self.no_track_attributes.add("player_specific_attributes")
        #self.exclude_from_dict.add("no_track_attributes")
        #self.exclude_from_dict.add("game_object_type")
        #self.exclude_from_dict.add("player_specific_attributes")

        self.player_specific_attributes = {}

        self.game_object_type = "None"

    def __setattr__(self, name, value):
        self.register_transition(name, value)
        super(StatefulGameObject, self).__setattr__(name, value)

    def register_transition(self, name, value, player=None):
        """
        This will register any changes in this object with the game.
        Notably, this will exclude anything in the no_track_attributes
        set.
        """

        if (hasattr(self, "game") and
                self.game is not None and
                name not in self.no_track_attributes):
            trans = ("set", self.game_object_type, self.game_id, name, value)
            self.game.add_transition(trans, player)

    def set_value(self, name, value, player=None):
        """
        Set values on this object. If the values can be public then it is
        better to use python attributes. If you need to set values on a specific
        player, then you can use this function.
        """
        if player is None:
            return setattr(self, name, value)

        self.player_specific_attributes.setdefault(player, {})[name] = value
        self.register_transition(name, value, player)

    def get_value(self, name, player=None):
        """
        Gets a value out of a stateful game object. This can be gotten on a
        player basis or, if player is None, this attempts to get the publicly
        avaliable information.
        """
        if player is None:
            if not hasattr(self, name):
                return None
            return getattr(self, name)
        vals = self.player_specific_attributes.get(player, None)
        if vals is not None:
            return vals.get(name, None)
        return None

    def to_dict(self, player=None):
        """
        This overrides the to_dict method from the GameObject class. If player
        is specified it will get all the state that pertains to that player;
        if player is None then it will only return data that is public
        information.
        """

        result = {x: y for x, y in self.__dict__.iteritems() if
                  x not in self.exclude_from_dict}
        # Add in everything for this specific player
        player_items = self.player_specific_attributes.get(player, {}).items()
        for key, value in player_items:
            result[key] = value

        return self.replace_game_objects(result)
