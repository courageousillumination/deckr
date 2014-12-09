"""
This module defines everything needed for the base Game class.
"""

from engine.card import Card
from engine.card_set import CardSet
from engine.decorators import game_serialize
from engine.exceptions import InvalidMoveException, NeedsMoreInfo
from engine.game_object import GameObject
from engine.mixins.configurable import Configurable
from engine.mixins.has_zones import HasZones
from engine.player import Player
from engine.zone import Zone


class Game(HasZones, Configurable):

    """
    A game is one of the core classes of the engine. It contains logic to run
    actions, check the game state, and calculate state transitions that are
    caused by specific actions.
    """

    def __init__(self):
        super(Game, self).__init__()

        """
        ######################
        # Complex Attributes #
        ######################

        # registered_objects is a dictionary of all objects that have been
        # registered with this game. It takes the following form.
        # { class1 : [next_id, {1 : object1, ...}],
        #   class2 : [next_id, {1 : object1, ...}]
        #   ...
        # }
        self.registered_objects = {}

        # The card set is only used in more complex games; it provides the
        # ability to generate cards on the fly easily.
        self.card_set = CardSet()

        # Playre zones is a list of all zones that should be give to every
        # player. This includes things like hands, decks, discards, etc.
        self.player_zones = []


        # transitions is a dictionary of lists of tuples. The dictionary keys
        # are player_ids and the values are lists of transitions that should be
        # visible to that player.
        # (< action >, < args >)
        # Where action is one of "move", "add", "remove", "set", "over"
        self.transitions = {}

        # steps are atomic units of what happens in a game.
        self.steps = []

        # This will store something akin to a state as we work our way through
        # the steps.
        self.current_kwargs = {}


        #####################
        # Simple attributes #
        #####################
        self.players = []
        self.max_players = 0
        self.min_players = 0
        self.is_set_up = False
        """

        #: Each element of this list is a dictionary representation of a zone
        #: that belongs to a player.
        self.player_zones = []
        #: Stores all registered objects.
        self.registered_objects = {}
        #: Stores the next avaliable game ID.
        self.next_game_id = 1
        #: All game transitions
        self.transitions = {}

    #############
    # Callbacks #
    #############

    def post_config_callback(self):
        """
        After we load the configuration we need to actually set up
        our card_set and zones.
        """

        self.card_set.load_from_list(self.card_set)

        game_zones = [x for x in self.zones if x.get('owner', None) is None]
        self.add_zones(game_zones)

    def add_zone_callback(self, new_zone):
        """
        Whenever we add a zone we need to register it.
        """

        self.register(new_zone)

    #####################
    # Registration code #
    #####################

    def register_single(self, obj):
        """
        Registers a single object.
        """

        if isinstance(obj, GameObject):
            obj.game_id = self.next_game_id
            obj.game = self

            self.registered_objects[self.next_game_id] = obj
            self.next_game_id += 1

    def deregister_single(self, obj):
        """
        Dergisters a single object.
        """

        if isinstance(obj, GameObject) and obj.game == self:
            del self.registered_objects[obj.game_id]

    def register(self, obj):
        """
        Registers an object by giving it a game_id. This will only
        allow you to register game objects. Can take either an iterable
        or a single object.
        """

        if hasattr(obj, '__iter__'):
            for o in obj:
                self.register_single(o)
        else:
            self.register_single(obj)

    def deregister(self, obj):
        """
        Removes either a single object or a list of objects.
        """

        if hasattr(obj, '__iter__'):
            for o in obj:
                self.deregister_single(o)
        else:
            self.deregister_single(obj)

    def get_object_with_id(self, game_id):
        """
        Gets an object with the given game_id. Returns None if no object is
        found.
        """

        return self.registered_objects.get(game_id, None)

    #############################
    # State and Transition code #
    #############################

    def add_transition(self, trans, player=None):
        """
        Add a transition to the current game state. If player is specified the
        transition will only apply to that player. Otherwise it will apply to
        all players.
        """

        if player is None:
            for p in self.players:
                self.transitions.setdefault(p, []).append(trans)
        else:
            self.transitions.setdefault(player, []).append(trans)

    def flush_transitions(self):
        """
        Flush all transitions. This should only be called in dire circumstances.
        """

        self.transitions = {}

    @game_serialize
    def get_transitions(self, player_id):
        """
        Requests the transitions for a specific player. This will implicitly
        flush the transitions for this player to ensure that we don't get
        duplicate transitions (although really they should be idempotent....)
        """

        result = self.transitions.get(player_id, [])
        self.transitions[player_id] = []
        return result

    @game_serialize
    def get_state(self, player_id=None):
        """
        This will return a list of all registerd objects in the game. This
        should be sufficent to reconstruct the entire game state.
        """

        return self.registerd_objects.values()

    ############################
    # Player manipulation code #
    ############################

    def check_can_add_player(self):
        if len(self.players) >= self.max_players:
            raise ValueError("Too many players.")
        if self.is_set_up:
            raise ValueError("Unable to join a game in progress")


    @game_serialize
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

        return player

    def remove_player(self, player_id):
        """
        Removes a player if possible and returns a
        boolean denoting success or failure
        """

        player = self.get_object_with_id(player_id)
        if player is not None and isinstace(player, Player):
            self.deregister(player)
            self.deregister(player.zones.values())
            self.players.remove(player)
            return True

        return False

    # TODO: Fix everything after this

    def substitute_kwargs(self, kwargs):
        """
        This function will perform some keyword argument substitutions. All the
        client knows about is GameIds, but here we only really care about
        objects. Instead of having to manually run self.get_object_with_id for
        every keyword argument we wanted to simplify the process. Thus, we
        automatically run these substitutions for some specific keyword
        arguments. Specifically:

            * If the keyword argument is card, cards or contains _card, _cards
              then it will be replaced with the corresponding Card object
            * If the keyword argument contains "zone" it will be replaced with
              a Zone object.
            * If the keyword argument contains "player" it will be replaced with
              a Player object.
        If the undelying object is a list it will try to perform the
        substitutions on each item of the list.
        """

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

        self.substitute_kwargs(kwargs)
        getattr(self, action_name)(**kwargs)

        # Run any steps that we can
        self.run()

        if self.is_over():
            self.add_transition(('is_over', self.winners()))



    def add_step(self, player, step, save_result_as=None, kwargs=None):
        """
        Registers a step that should be run.
        """

        self.steps.append((step, player, save_result_as, kwargs))

    def run(self):
        """
        This will run all steps until it is impossible to do so anymore. The
        output of the step can be stored, and we pass in the current list of
        all my keyword argumnets to the step. This allows steps to communicate
        with one another.
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

        # If we get down here we're not really expecting any action and we can
        # clear out all of the state.
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

    # pylint: disable=unused-argument
    def send_information_restriction(self, player, **kwargs):
        """
        We can only send information if the server is expecting it from this
        player.
        """

        if self.expected_action is None:
            return False
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
