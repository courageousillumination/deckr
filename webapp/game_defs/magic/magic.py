
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

            self.register(deck)
            player.library.set_cards(deck)

        # Perform actual set up
        for player in self.players:
            for _ in range(STARTING_HAND_SIZE):
                self.draw_card(player)

            player.life = 20

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

    def has_priority(self, player):
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
            # Change active player here
            pass
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
