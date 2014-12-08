
"""
This module provides an implementation of Magic: The Gathering.
"""

from engine.game import Game

STARTING_HAND_SIZE = 7

class Magic(Game):
    """
    Magic: The Gathering.
    """

    def __init__(self):
        super(Magic, self).__init__()
        self.deck1 = [("Island", 30)]
        self.deck2 = [("Forest", 30)]

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

    def is_over(self):
        pass

    def winners(self):
        pass

    ###############
    # Other stuff #
    ###############

    def move_card(self, card, target_zone):
        # Account for visibility here
        target_zone.push(card)

    def draw_card(self, player):
        self.move_card(player.library.pop(), player.hand)
