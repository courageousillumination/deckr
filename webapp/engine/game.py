"""
This module defines everything needed for the base Game class.
"""

from engine.card import Card
from engine.card_set import CardSet
from engine.has_zones import HasZones
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

    def __init__(self, requirement=None):
        super(NeedsMoreInfo, self).__init__()
        self.requirement = requirement

    def __str__(self):
        return "Need more information for {0}".format(self.requirement)


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

    Each argument to requires should be a tuple of the following form:

        parameter_name, expected_type, test, (String)

    The final argument is optional. If given it will be returned to the client
    to give them some idea of what is being asked for.
    """

    def wrapper(func):
        """
        Woo decorators!
        """

        def inner(*args, **kwargs):
            """
            MOAR decorators!
            """

            if requires is not None:
                for requirement in requires:
                    # Check if we have it in kwargs
                    value = kwargs.get(requirement[0], None)
                    if value is None:
                        raise NeedsMoreInfo(requirement)
                    # Make sure we pass the test
                    if not requirement[2](*args, **kwargs):
                        raise NeedsMoreInfo(requirement)

            return func(*args, **kwargs)
        return inner
    return wrapper


class Game(HasZones):

    """
    A game is one of the core classes of the engine. It contains logic to run
    actions, check the game state, and calculate state transitions that are
    caused by specific actions.
    """

    def __init__(self):
        super(Game, self).__init__()

        # registered_objects is a dictionary of all objects that have been
        # registered with this game. It takes the following form.
        # { class1 : [next_id, {1 : object1, ...}],
        #   class2 : [next_id, {1 : object1, ...}]
        #   ...
        # }
        self.registered_objects = {}
        self.player_zones = []
        self.max_players = 0
        self.min_players = 0
        self.players = []
        self.card_set = CardSet()

        # transitions is a dictionary of lists of tuples. The dictionary keys
        # are player_ids and the values are lists of transitions that should be
        # visible to that player.
        # (< action >, < args >)
        # Where action is one of "move", "add", "remove", "set", "over"
        self.transitions = {}

        # Steps....
        self.steps = []
        self.expected_action = None
        self.current_kwargs = {}

    def load_config(self, config):
        """
        This will load a game from a configuration_file.
        Somebody else should do the parsing and pass the config a dictionary
        that defines the configuration of the game.
        """

        self.max_players = config.get('max_players', 0)
        self.min_players = config.get('min_players', 0)

        zones = config.get('zones', [])
        self.card_set.load_from_list(config.get('card_set', []))

        game_zones = [x for x in zones if x.get('owner', None) is None]
        player_zones = [x for x in zones if x.get('owner', None) == 'player']
        self.add_zones(game_zones)
        self.player_zones = player_zones

        # Register all zones
        self.register(self.zones.values())

    def make_action(self, action_name, **kwargs):
        """
        This will try to make an action with the specified
        keyword arguments. It will look at all internal functions
        that have the @action and attempt to run the first one that
        matches. If the action is invalid this could throw an exception.
        """

        # Flush the old transitions
        self.flush_transitions()

        if (not hasattr(self, action_name) or
                (self.expected_action is not None and
                 action_name != self.expected_action[0])):
            raise InvalidMoveException

        # We make some substitutions in the kwargs. These can be a little
        # dangerous, but generally make life a lot easier later on.
        for key, value in kwargs.items():
            if ("card" == key or "_card" in key or
                    "cards" == key or "_cards" in key):
                object_type = "Card"
            elif "zone" in key:
                object_type = "Zone"
            elif "player" in key:
                object_type = "Player"
            else:
                continue
            if isinstance(kwargs[key], list):
                kwargs[key] = [self.get_object_with_id(object_type, int(x))
                               for x in kwargs[key]]
            else:
                kwargs[key] = self.get_object_with_id(object_type, int(value))
        getattr(self, action_name)(**kwargs)

        # Run any steps that we can
        self.run()

        if self.is_over():
            self.add_transition(('is_over', self.winners()))

    def deregister(self, objects):
        """
        This function will deregister objects in the game, cleaning up anything
        that register created.
        """

        for obj in objects:
            if obj.game_id is None:
                continue

            if isinstance(obj, Card):
                object_type = "Card"
            elif isinstance(obj, Zone):
                object_type = "Zone"
            elif isinstance(obj, Player):
                object_type = "Player"
            else:
                object_type = type(obj).__name__

            if object_type in self.registered_objects:
                del self.registered_objects[object_type][1][obj.game_id]
                self.registered_objects[object_type][0] -= 1

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

    def add_transition(self, trans, player=None):
        """
        Add a tuple to the current list of transitions. If player is given it
        will register it as a player specific transition. Otherwise it registers
        as a global transition.
        """

        if player is None:
            key = None
        else:
            key = player.game_id

        self.transitions.setdefault(key, []).append(trans)

    def get_public_transitions(self):
        """
        Get all the transitions that have been registered without a player.
        """

        return self.transitions.get(None, [])

    def get_player_transitions(self, player_id):
        """
        Get all the transitions that have been registered for a specific player.
        """

        return self.transitions.get(player_id, [])

    def flush_transitions(self):
        """
        Get rid of all the current transitions.
        """

        self.transitions = {}

    def remove_player(self, player_id):
        """
        Removes a player if possible and returns a
        boolean denoting success or failure
        """
        player = self.get_object_with_id("Player", player_id)
        if player is None:
            return False
        self.deregister([player])
        self.deregister(player.zones.values())
        for name in player.zones:
            del self.zones[name + '_' + str(player.game_id)]
        self.players.remove(player)
        return True

    def add_player(self):
        """
        Adds a player if possible and returns the player id
        """

        if len(self.players) >= self.max_players:
            raise ValueError("Too many players.")

        player = Player()
        player.add_zones(self.player_zones)
        self.players.append(player)

        # Register both the player and it's zones with the game.
        self.register([player])
        self.register(player.zones.values())
        # Add the per-player zones to our dictionary and add the owner to
        # each zone.
        for name, zone in player.zones.items():
            zone.owner = player
            zone_name = name + '_' + str(player.game_id)
            self.zones[zone_name] = zone
            setattr(self, zone_name, zone)
        return player.game_id

    def get_state(self, player_id=None):
        """
        This will return a dictonary containg the game state. This includes
        all cards and all their data, all zones, all players and their
        attributes, etc.
        """

        if player_id is not None:
            player = self.get_object_with_id("Player", player_id)
        else:
            player = None

        # Get all of my objects
        _, cards = self.registered_objects.get("Card", (1, {}))
        _, zones = self.registered_objects.get("Zone", (1, {}))
        _, players = self.registered_objects.get("Player", (1, {}))

        # Convert to a dictionary
        result = {}

        result['cards'] = [x.to_dict(player) for x in cards.values()]
        result['players'] = [x.to_dict(player) for x in players.values()]
        # Note that zones aren't StatefulGameObjects but just base game
        # objects.
        result['zones'] = [x.to_dict() for x in zones.values()]

        return result

    def add_step(self, player, step, save_result_as=None, kwargs=None):
        """
        Registers a step that should be run.
        """

        self.steps.append((step, player, save_result_as, kwargs))

    def run(self):
        """
        This will run all steps until it is impossible to do so anymore.
        """

        while len(self.steps) > 0:
            step, player, save_result_as, kwargs = self.steps[0]
            # See if the step has any specific arguments that should
            # be passed in.
            if kwargs is None:
                all_kwargs = self.current_kwargs
            else:
                all_kwargs = dict(kwargs.items() + self.current_kwargs.items())
            # Try to run the step, catching any NeedsMoreInfo execptions that
            # are raised
            try:
                result = step(player, **all_kwargs)
            except NeedsMoreInfo as exception:
                if len(exception.requirement) > 3:
                    message = exception.requirement[3]
                else:
                    message = "Need more information"
                self.expected_action = ("send_information",
                                        exception.requirement[0],
                                        exception.requirement[1],
                                        player.game_id,
                                        message)
                return

            if save_result_as is not None:
                self.current_kwargs[save_result_as] = result
            # Now that it's actually been resovled we can clear it
            self.steps.pop(0)

        # If we get down here we're not really expecting any action.
        self.expected_action = None
        self.current_kwargs = {}

    def abandon_ship(self):
        """
        Clear all kwargs and steps. Reset to a blank state. This should really
        only be used in development.
        """

        self.expected_action = None
        self.current_kwargs = {}
        self.steps = []

    def get_expected_action(self):
        """
        This can give the client a hint about what is supposed to happen
        next.
        """

        return self.expected_action

    def clear_keyword_argument(self, key):
        """
        Remove a keyword argument from the current arguments being passed into
        the steps. This can be needed when a step needs to get the value
        multiple times.
        """

        if self.current_kwargs.get(key, None) is not None:
            del self.current_kwargs[key]

    # pylint: disable=unused-argument
    def send_information_restriction(self, player, **kwargs):
        """
        We can only send information if the server is expecting it.
        """

        return player.game_id == self.expected_action[3]

    @action(restriction=send_information_restriction)
    def send_information(self, player, **kwargs):
        """
        This is a bulit in action to send more information. This will update
        the current information and then return, hoping that self.run will
        continue where it left off.
        """

        for key, value in kwargs.items():
            self.current_kwargs[key] = value

    @game_step(requires=None)
    def clear_keyword_step(self, player, key, **kwargs):
        """
        Sometimes we need to clean up the kwargs in the steps. This facilitates
        that.
        """

        self.clear_keyword_argument(key)

    @game_step(requires=None)
    def clear_all_keywords(self, player, **kwargs):
        """
        This will allow the entire dictionary to be cleared at some point.
        """

        self.current_kwargs = {}
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
