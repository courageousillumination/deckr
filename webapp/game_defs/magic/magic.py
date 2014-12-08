
"""
This module provides an implementation of Magic: The Gathering.
"""

from engine.game import action, Game
from engine.stateful_game_object import StatefulGameObject

STARTING_HAND_SIZE = 7
PHASE_ORDER = [
    ("beginning", "untap"),
    ("beginning", "upkeep"),
    ("beginning", "draw"),

    ("precombat_main", None),

    ("combat", "beginning_of_combat"),
    ("combat", "declare_attackers"),
    ("combat", "declare_blockers"),
    ("combat", "deal_combat_damage"),
    ("combat", "end_of_combat"),

    ("postcombat_main", None),

    ("end", "end"),
    ("end", "cleanup")
]


def create_mana_from_string(mana_string):
    """
    Creates a Mana object from a string.
    """

    blue = mana_string.count('U')
    white = mana_string.count('W')
    black = mana_string.count('B')
    red = mana_string.count('R')
    green = mana_string.count('G')
    #colorless = mana_string.count('U')
    return Mana(red, blue, green, white, black)

class Mana(object):
    """
    Represents a mana cost, pool, etc.
    """

    def __init__(self, red = 0, blue = 0, green = 0,
                 white = 0, black = 0, colorless = 0):
        """
        Creates a Mana object with the given values. Will raise a ValueError
        exception if any of the numbers are negative.
        """

        if red < 0 or blue < 0 or green < 0 or white < 0 or black < 0 or colorless < 0:
            raise ValueError("Mana can only be created with a positive number")

        self.red = red
        self.blue = blue
        self.green = green
        self.white = white
        self.black = black
        self.colorless = colorless

    def converted_mana(self):
        return (self.red + self.blue + self.green + self.white + self.black +
                self.colorless)

    def __add__(self, other):
        """
        Here we override add to just combine two mana objects.
        """

        return Mana(red = self.red + other.red,
                    blue = self.blue + other.blue,
                    green = self.green + other.green,
                    white = self.white + other.white,
                    black = self.black + other.black,
                    colorless = self.colorless + other.colorless)


    def __sub__(self, other):
        """
        Here we override subtract to work on a component by component basis
        """

        return Mana(red = self.red - other.red,
                    blue = self.blue - other.blue,
                    green = self.green - other.green,
                    white = self.white - other.white,
                    black = self.black - other.black,
                    colorless = self.colorless - other.colorless)

    def __str__(self):
        return ("W" * self.white + "U" * self.blue + "B" * self.black +
                "R" * self.red + "G" * self.green)

class Magic(Game):
    """
    Magic: The Gathering.
    """

    def __init__(self):
        super(Magic, self).__init__()
        self.deck1 = [("Island", 30)]
        self.deck2 = [("Forest", 30)]

        self.step = None
        self.phase = None
        self.active_player = None
        self.has_priority_player = None
        self.attacking = False
        self.has_played_land = False

    ##################
    # Base functions #
    ##################

    def set_up(self):
        decks_and_players = [(self.deck1, self.players[0]),
                             (self.deck2, self.players[1])]

        for deck_list, player in decks_and_players:
            deck = []
            for card, num in deck_list:
                deck += self.card_set.create(card, num)

            for card in deck:
                card.tapped = False

            self.register(deck)
            player.library.set_cards(deck)

        # Perform actual set up
        for player in self.players:
            for _ in range(STARTING_HAND_SIZE):
                self.draw_card(player)

            player.life = 20
            player.mana_pool = Mana()

        self.phase = "beginning"
        self.step = "upkeep"
        self.active_player = self.players[0]
        self.has_priority_player = self.players[0]

    def is_over(self):
        return False # TODO

    def winners(self):
        return [] # TODO

    ###########
    # Actions #
    ###########

    def play_card_restriction(self, player, card):
        if not self.has_priority_player == player:
            return False

        if "Land" in card.types:
            if not (not self.has_played_land and
                    "main" in self.phase and
                    self.stack.get_num_cards() == 0):
                return False

        return True

    @action(restriction = play_card_restriction)
    def play_card(self, player, card):

        # Deal with Lands since they're a special case.
        if "Land" in card.types:
            self.move_card(card, player.battlefield)
            self.has_played_land = True

    def has_priority(self, player, *args, **kwargs):
        return self.has_priority_player == player

    @action(restriction = has_priority)
    def pass_priority(self, player):
        """
        Pass the priority on to the next player.
        """

        next_player = self.get_next_player(player)
        if (next_player == self.active_player and
            self.stack.get_num_cards() == 0):
            self.next_phase_or_step()
        else:
            self.has_priority_player = next_player


    @action(restriction = has_priority)
    def activate_ability(self, player, card):
        """
        Activates the ability for a specific card.
        """

        # First we have to pay the cost
        cost, result = card.ability.split(':')

        if (cost == "{T}"):
            card.tapped = True

        # Then we resolve the ability
        if ("Land" in card.types):
            player.mana_pool += create_mana_from_string(result)


    ###############
    # Other stuff #
    ###############

    def next_phase_or_step(self):
        """
        Move on to the next phase or step.
        """

        index = PHASE_ORDER.index((self.phase, self.step))

        # TODO: This should probably use a game_step or something so we can
        # insert triggers (when that's working....)

        # Deal with edge cases
        if self.step == "declare_attackers" and not self.attacking:
            self.step = "end_of_combat"
        elif self.step == "cleanup":
            # Clean up all global state
            self.has_played_land = False
            self.attacking = False
        else:
            next_phase, next_step = PHASE_ORDER[index + 1]
            self.step = next_step
            self.phase = next_phase

        self.has_priority_player = self.active_player

    def get_next_player(self, player):
        """
        Gets the next player after a specific player in the turn order.
        """

        player_index = self.players.index(player)
        if player_index == (len(self.players) - 1):
            return self.players[0]
        else:
            return self.players[player_index + 1]


    def move_card(self, card, target_zone):
        # Account for visibility here
        target_zone.push(card)

    def draw_card(self, player):
        self.move_card(player.library.pop(), player.hand)
