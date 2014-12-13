"""
This module defines everything needed for the base Game class.
"""

from engine.core.decorators import game_serialize
from engine.core.game_object import GameObject
from engine.core.player import Player
from engine.mixins.configurable import Configurable
from engine.mixins.has_zones import HasZones


class Game(GameObject, HasZones, Configurable):

    """
    A game is one of the core classes of the engine. It contains logic to run
    actions, check the game state, and calculate state transitions that are
    caused by specific actions.
    """

    def __init__(self):
        super(Game, self).__init__()

        #: Each element of this list is a dictionary representation of a zone
        #: that belongs to a player.
        self.player_zones = []
        #: Stores all registered objects.
        self.registered_objects = {}
        #: Stores the next avaliable game ID.
        self.next_game_id = 0
        #: All game transitions
        self.transitions = {}
        #: This stores the cardset for this Game. Can be None if the game
        #: doesn't define a card set.
        self.card_set = None

        self.players = []
        self.max_players = 0
        self.min_players = 0
        self.is_set_up = False

        # Note that since a game is a GameObject we need to make sure it
        # starts off in the right state. Having a node point to itself is
        # pretty ugly, but necessary here.
        self.register(self)

        # Set up the configuration for a game.
        self.required_fields.add('min_players')
        self.required_fields.add('max_players')
        self.default_values['game_zones'] = []
        self.default_values['player_zones'] = []

    #############
    # Callbacks #
    #############

    def post_config_callback(self):
        """
        After we load the configuration we need to actually set up
        our card_set and zones.
        """

        self.add_zones(self.game_zones)

    def add_zone_callback(self, new_zone):
        """
        Whenever we add a zone we need to register it.
        """

        print new_zone
        self.register(new_zone)

    #####################
    # Registration code #
    #####################

    def register_single(self, obj):
        """
        Registers a single object. Input should be checked elsewher to make
        sure that it is a GameObject
        """

        obj.game_id = self.next_game_id
        obj.game = self

        self.registered_objects[self.next_game_id] = obj
        self.next_game_id += 1

    def deregister_single(self, obj):
        """
        Dergisters a single object.
        """

        if (obj.game == self and obj.game_id in self.registered_objects):
            del self.registered_objects[obj.game_id]

    def register(self, obj):
        """
        Registers an object by giving it a game_id. This will only
        allow you to register game objects. Can take either an iterable
        or a single object.
        """

        if isinstance(obj, GameObject):
            self.register_single(obj)
        elif hasattr(obj, '__iter__'):
            for o in obj:
                if isinstance(o, GameObject):
                    self.register_single(o)


    def deregister(self, obj):
        """
        Removes either a single object or a list of objects.
        """

        if isinstance(obj, GameObject):
            self.deregister_single(obj)
        elif hasattr(obj, '__iter__'):
            for o in obj:
                if isinstance(o, GameObject):
                    self.deregister_single(o)

    def get_object_with_id(self, game_id, klass = None):
        """
        Gets an object with the given game_id. Returns None if no object is
        found. Takes in an optional klass argument. If the object is expected
        to be of the given class but it is not then it returns None.
        """

        result = self.registered_objects.get(game_id, None)
        if (result is not None and
            (klass is None or isinstance(result, klass))):
            return result
        return None

    #############################
    # State and Transition code #
    #############################

    def add_transition(self, trans, player_id=None):
        """
        Add a transition to the current game state. If player is specified the
        transition will only apply to that player. Otherwise it will apply to
        all players.
        """

        if player_id is None:
            for p in self.players:
                self.transitions.setdefault(p.game_id, []).append(trans)
        else:
            self.transitions.setdefault(player_id, []).append(trans)

    @game_serialize
    def get_transitions(self, player_id):
        """
        Requests the transitions for a specific player. This will implicitly
        flush the transitions for this player to ensure that we don't get
        duplicate transitions (although really they should be idempotent....)
        """

        result = self.transitions.get(player_id, [])
        # In theory these could be flushed somewhere for future playback
        self.transitions[player_id] = []
        return result

    @game_serialize
    def get_state(self, player_id=None):
        """
        This will return a list of all registerd objects in the game. This
        should be sufficent to reconstruct the entire game state.
        """

        return self.registered_objects.values()

    ############################
    # Player manipulation code #
    ############################

    def check_can_add_player(self):
        if len(self.players) >= self.max_players:
            raise ValueError("Too many players.")
        if self.is_set_up:
            raise ValueError("Unable to join a game in progress")


    def add_player(self):
        """
        Adds a player if possible, returning the newly added player
        """

        self.check_can_add_player()

        player = Player()
        player.add_zones(self.player_zones)

        # Update all the game state.
        self.register(player)
        self.register(player.zones.values())
        self.players.append(player)

        return player.game_id

    def remove_player(self, player_id):
        """
        Removes a player if possible. If the player is not currently registered
        then it fails silently.
        """

        player = self.get_object_with_id(player_id, Player)
        if player is not None:
            self.deregister(player)
            self.deregister(player.zones.values())
            self.players.remove(player)

    ##################################
    # Code for running Actions/Steps #
    ##################################

    def make_action(self, action_name, **kwargs):
        """
        This will try to make an action with the specified
        keyword arguments. It will look at all internal functions
        that have the @action and attempt to run the first one that
        matches. If the action is invalid this could throw an exception.
        """

        # Make sure the action is expected right now.

        # Run the action
        getattr(self, action_name)(**kwargs)

        # Run any steps that have been created by the action
        self.run()

        # Finally check if we're over and respond appropriatly.
        if self.is_over():
            self.add_transition(('is_over', self.winners()))

    def run(self):
        """
        TODO: Update this
        """

        while len(self.steps) > 0:
            current_step = self.steps[0]
            current_step.run(self)
            self.steps.pop(0)

        # Clear out everything at the end

    def abandon_ship(self):
        """
        Clear all kwargs and steps. Reset to a blank state. This can be used
        when something goes terribly wrong.
        """

        pass


    ###############
    # Set up code #
    ###############

    def has_enough_players(self):
        """
        Returns true if num players >= min_players
        """

        return len(self.players) >= self.min_players

    def set_up_wrapper(self):
        """
        This will simply wrap the subclass set_up, but also perform some
        validation and book keeping. This should be called from the game runner.
        """

        if (not self.has_enough_players()) or self.is_set_up:
            return False
        self.set_up()
        self.is_set_up = True
        return True

    #############################
    # Default actions and steps #
    #############################


    ####################################
    # Functions that must be overriden #
    ####################################

    def set_up(self):
        """
        This will set up the actual game. This includes dealing cards, setting
        up state, etc. This should be used over __init__.
        """

        raise NotImplementedError

    def is_over(self):
        """
        This function will be called after every action to see if the game
        is over.
        """

        raise NotImplementedError

    def winners(self):
        """
        This should return the list of winners assuming that the game is over.
        """

        raise NotImplementedError