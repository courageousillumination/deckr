"""
This module defines the GameObject.
"""


class GameObject(object):

    """
    A GameObject is any object in the game.
    """

    def __init__(self):
        # This is the ID of **this** object in the game.
        self.game_id = None
        # This is the actual game object that this belongs to.
        self.game = None
        # Values that should be excluded from a dictonary definition
        self.exclude_from_dict = set()
        self.exclude_from_dict.add('game')
        self.exclude_from_dict.add("exclude_from_dict")

    def replace_game_objects(self, item):
        """
        This will take in an arbitrary item and try to replace any
        GameObjects with their ids. This works over iterables and dictonaries
        """

        # If it's just a raw GameObject do the substitution
        if isinstance(item, GameObject):
            return item.game_id
        # If it's a dictionary we replace each sub item.
        elif isinstance(item, dict):
            new_items = {}
            for key, value in item.items():
                converted_key = self.replace_game_objects(key)
                new_items[converted_key] = self.replace_game_objects(value)
            return new_items
        # If it's iterable we return a list of the replaced items
        elif hasattr(item, "__iter__"):
            return [self.replace_game_objects(x) for x in item]
        # If none of the above are true we just return the item.
        else:
            return item

    # This is overriden by stateful game objets which care about what player
    # we are.
    def to_dict(self, player=None):  # pylint: disable=unused-argument
        """
        Converts a GameObject into a dictonary, excluding various values
        and using game_ids where possible.
        """

        result = {x: y for x, y in self.__dict__.iteritems() if
                  x not in self.exclude_from_dict}
        return self.replace_game_objects(result)
