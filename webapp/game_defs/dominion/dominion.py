
"""
This module provides an implementation of a game of Dominion
"""

from engine.game import Game


class Dominion(Game):
    """
    Dominion is a more complex card game.
    """

    def __init__(self):
        super(Dominion, self).__init__()

    def set_up(self):
        import random

        # Select 10 random kindom cards
        all_kingdom_cards = [x for x in self.card_set.all_cards() if
                             x["kingdom_card"]]
        kingdom_cards = random.sample(all_kingdom_cards, 10)
        for i in range(10):
            cards = self.card_set.create(kingdom_cards[i]["name"], 10)
            self.kingdom[i].set_cards(cards)
            self.register(cards)

        # Create treasures, victory and curses.
        cards_to_zones = [('Curse', 'curses', (len(self.players) - 1)* 10),
                          ('Estate', 'victory0', 12),
                          ('Duchy', 'victory1', 12),
                          ('Province', 'victory2', 12),
                          ('Copper', 'treasure0', 60 - 7 * len(self.players)),
                          ('Silver', 'treasure1', 40),
                          ('Gold', 'treasure2', 30),
                          ]

        for card, zone, num in cards_to_zones:
            cards = self.card_set.create(card, num)
            self.zones[zone].set_cards(cards)
            self.register(cards)

        # Give each player a deck
        for player in self.players:
            deck = (self.card_set.create("Copper", 7) +
                    self.card_set.create("Estate", 3))
            random.shuffle(deck)
            player.deck.set_cards(deck)
            self.register(deck)
            for _ in range(5):
                self.draw(player)

    def is_over(self):
        """
        Dominion is over if the provinces are out or three supply piles are
        out.
        """

        return False


    def winners(self):
        """
        Count up victory points for each player
        """

        return []

    def draw(self, player):
        if player.deck.get_num_cards() == 0:
            if player.discard.get_num_cards() == 0:
                return
            # Trigger a reshuffle
            while player.discard.get_num_cards() > 0:
                card = player.discard.pop()
                card.face_up = False
                card.set_value("face_up", False, player)
                player.deck.push(card)
            player.deck.shuffle()
        card = player.deck.pop()
        card.set_value("face_up", True, player)
        player.hand.push(card)

    """
    def next_player(self, player):
        player_index = self.players.index(player)
        print self.players
        print player_index
        if player_index == (len(self.players) - 1):
            return self.players[0]
        else:
            return self.players[player_index + 1]

    @action(restriction=can_play_card)
    def play_card(self, player, card):
        player.hand.remove_card(card)
        self.play_zone.add_card(card)

        card.face_up = True
        if self.play_zone.suit is None:
            self.play_zone.suit = card.suit

        self.current_turn = self.next_player(player)

        if card.number == 2 and card.suit == 'clubs':
            self.played_two_of_clubs = True


    @action(restriction=can_take_trick)
    def take_trick(self, player):
        contains_point_card = False
        while self.play_zone.get_num_cards() > 0:
            card = self.play_zone.pop()
            card.face_up = False
            card.set_value("face_up", False, card.owner)
            player.discard.push(card)

            if (card.suit == 'hearts' or
                card.suit == 'spades' and card.number == 12):
                contains_point_card = True
            if not self.hearts_broken and contains_point_card:
                self.hearts_broken = True


        self.play_zone.suit = None
        self.current_turn = player

        # Check if we need to take anything from the side_zone
        if self.side_zone.get_num_cards() > 0 and contains_point_card:
            while self.side_zone.get_num_cards() > 0:
                player.discard.push(self.size_zone.pop())

        """
