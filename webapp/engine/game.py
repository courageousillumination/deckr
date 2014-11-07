"""
This module defines everything needed for the base Game class.
"""

from engine.zone import Zone


class InvalidMoveException(Exception):

    """
    This will be raised whenever a player makes an invalid move.
    """

    def __init__(self, value):
        super(InvalidMoveException, self).__init__()
        self.value = value

    def __str__(self):
        return repr(self.value)


def action(restriction=None):
    """
    This is a decorator that can be put around actions in Game subclasses.
    restrictions is an optional function that takes the same arguments as
    the original function and returns a bool. If restrictions returns false
    the action will raise an exception.
    """

    def wrapper(func):
        """
        Part of the wrapper to make the decorator work.
        """

        def inner(*args, **kwargs):
            """
            Yet another part of the decorator.
            """

            if restriction is None or restriction(*args, **kwargs):
                return func(*args, **kwargs)
            else:
                raise InvalidMoveException("Invalid Move")
        return inner
    return wrapper


class Game(object):

    """
    A game is one of the core classes of the engine. It contains logic to run
    actions, check the game state, and calculate state transitions that are
    caused by specific actions.
    """

    def __init__(self):
        # registered_objects is a dictionary of all objects that have been
        # registered with this game. It takes the following form.
        # { class1 : [next_id, {1 : object1, ...}],
        #   class2 : [next_id, {1 : object1, ...}]
        #   ...
        # }
        self.registered_objects = {}
        self.zones = {}
        self.max_players = 0

        # transitions will be a list of tuples of the following form:
        # (< action >, < args >)
        # Where action is one of "move", "add", "remove", "set", "over"
        self.transitions = []

    def load_config(self, config):
        """
        This will load a game from a configuration_file.
        Somebody else should do the parsing and pass the config a dictionary
        that defines the configuration of the game.
        """

        self.max_players = config.get('max_players', 0)
        zones = config.get('zones', [])

        for zone in zones:
            zone_object = Zone()
            zone_object.stacked = zone.get('stacked', False)

            # Add to the zones dictionary
            self.zones[zone["name"]] = zone_object
            # Add an attribute
            setattr(self, zone["name"], zone_object)

        # Register all zones
        self.register(self.zones.values())

    def make_action(self, action_name, **kwargs):
        """
        This will try to make an action with the specified
        keyword arguments. It will look at all internal functions
        that have the @action and attempt to run the first one that
        matches. If the action is invalid this could throw an exception.
        """

        if not hasattr(self, action_name):
            return False

        try:
            getattr(self, action_name)(**kwargs)
        except InvalidMoveException:
            return False

        #transitions = self.get_transitions()
        # self.flush_transitions()
        # return transitions
        return True

    def register(self, objects):
        """
        This function will register objects in the game. Each object will
        be given a unique id (unique within its class). Objects that already
        have an id will not be assigned a new one.
        """

        for obj in objects:
            # Don't bother re registering
            if obj.game_id is not None:
                continue

            object_type = type(obj)
            if object_type not in self.registered_objects:
                self.registered_objects[object_type] = [2, {1: obj}]
                obj.game_id = 1
            else:
                next_id = self.registered_objects[object_type][0]
                self.registered_objects[object_type][1][next_id] = obj
                self.registered_objects[object_type][0] = next_id + 1
                obj.game_id = next_id

            obj.game = self

    def get_object_with_id(self, klass, game_id):
        """
        Gets an internal object of the given class with the given id. If
        the object isn't found this just return None.
        """

        try:
            return self.registered_objects[klass][1][game_id]
        except KeyError:
            return None

    def add_transition(self, trans):
        """
        Add a tuple to the current list of transitions.
        """

        self.transitions.append(trans)

    def get_transitions(self):
        """
        Get all the changes that have occured since the changes were
        last flushed.
        """

        return self.transitions

    def flush_transitions(self):
        """
        Get rid of all the current transitions.
        """

        self.transitions = []

    # Actions after this point should be implemented by subclasses

    def set_up(self):
        """
        This will set up the actual game. This includes dealing cards, setting
        up state, etc. This should be used over __init__.
        """

        pass

    def is_over(self):
        """
        This function will be called after every action to see if the game
        is over.
        """

        pass
