"""
This module defines everything needed for the base Game class.
"""

from engine.card import Card
from engine.player import Player
from engine.zone import Zone


class InvalidMoveException(Exception):

    """
    This will be raised whenever a player makes an invalid move.
    """

    def __init__(self, value=None):
        super(InvalidMoveException, self).__init__()
        self.value = value

    def __str__(self):
        return repr(self.value)


class NeedsMoreInfo(Exception):

    """
    This can be thrown by a step that needs more information before it can
    continue.
    """

    pass


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


def game_step(requires=None):
    """
    A step is a subcomponent of an action. Actions are things that the user can
    do while, steps are things that result from actions. An action ought to have
    one or more steps. A step can require more input, in which case the user
    is prompted. Once the user returns with more input the step continues where
    it left off.

    If requires is None will just run the step; otherwise it checks to see if
    it has the required values. If it doesn't it throws a NeedsMoreInfo
    exception.
    """

    def wrapper(func):
        """
        Woo decorators!
        """

        def inner(*args, **kwargs):
            """
            MOAR decorators!
            """

            return func(*args, **kwargs)
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
        self.player_zones = []
        self.max_players = 0
        self.players = []

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
            zone_object.name = zone.get('name', '')
            zone_object.zone_type = zone.get('zone_type', '')

            # TODO: Do we want zones to store these? It's only useful here,
            # as far as I can tell, if we use tuples later.
            zone_object.owner = zone.get('owner', '')
            zone_object.multiplicity = zone.get('multiplicity', 1)

            # We need to keep track of the zones that
            # need to be given to players later on
            if(zone_object.owner == 'player'):
                self.player_zones.append(tuple(zone_object, zone_object.multiplicity))
            else:
                # We can deal with multiplicity here, otherwise
                for i in range(0, zone_object.multiplicity):
                    # We only want to number a zone if there will be
                    # more than one of it.
                    if(zone_object.multiplicity == 1):
                        mult = ''
                    else:
                        mult = str(i)

                    # Add to the zones dictionary
                    self.zones[zone["name"] + mult] = zone_object
                    # Add an attribute
                    setattr(self, zone["name"] + mult, zone_object)

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
            raise InvalidMoveException

        # We make some substitutions in the kwargs
        for key, value in kwargs.items():
            if "card" in key:
                kwargs[key] = self.get_object_with_id("Card", int(value))
            elif "zone" in key:
                kwargs[key] = self.get_object_with_id("Zone", int(value))
            elif "player" in key:
                kwargs[key] = self.get_object_with_id("Player", int(value))

        getattr(self, action_name)(**kwargs)

        transitions = self.get_transitions()
        if self.is_over():
            self.add_transition(('is_over', self.winners()))

        self.flush_transitions()
        return transitions

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

            if isinstance(obj, Card):
                object_type = "Card"
            elif isinstance(obj, Zone):
                object_type = "Zone"
            elif isinstance(obj, Player):
                object_type = "Player"
            else:
                # If it's not one of the above we just
                # use the class name.
                object_type = type(obj).__name__

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

    def remove_player(self, player_id):
        """
        Removes a player if possible and returns a
        boolean denoting success or failure
        """
        pass

    def add_player(self):
        """
        Adds a player if possible and returns the player id
        """

        if len(self.players) >= self.max_players:
            raise ValueError("Too many players.")

        player = Player()
        player.zones = {}

        for (zone, multiplicity) in self.player_zones:
            # Give the zone an owner
            zone.owner = player

            # Make a bunch of copies, if necessary
            id_str = ''
            for i in range(0, multiplicity):
                if multiplicity != 1:
                    id_str = str(i)

                # Add zone to player's dictionary
                player.zones[zone.name + mult] = zone
                # Make it an attribute
                setattr(player, zone.name + mult, zone)

                # Add to the zones dictionary
                self.zones["name_" + player.game_id + mult] = zone
                # TODO: Do we still want an attribute for this? 
                setattr(self, zone.name + player.game_id + mult, zone)


        self.register([player])
        self.register(player.zones.values())
        self.players.append(player)

        return player.game_id

    def get_state(self):
        """
        This will return a dictonary containg the game state. This includes
        all cards and all their data, all zones, all players and their
        attributes, etc.
        """

        # Get all of my objects
        _, cards = self.registered_objects.get("Card", (1, {}))
        _, zones = self.registered_objects.get("Zone", (1, {}))
        _, players = self.registered_objects.get("Player", (1, {}))

        # Convert to a dictionary
        result = {}

        print cards
        result['cards'] = [x.to_dict() for x in cards.values()]
        result['zones'] = [x.to_dict() for x in zones.values()]
        result['players'] = [x.to_dict() for x in players.values()]

        return result

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
