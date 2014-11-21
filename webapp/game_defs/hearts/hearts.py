"""
This module provides an implementation of a game of Solitaire
"""

from engine.card import Card
from engine.game import action, Game

SUITS = ["clubs", "spades", "hearts", "diamonds"]

def get_file_name(suit, number):
    if number == 14:
        return str(SUITS.index(suit) + 1) + ".png"

    dist_from_top = (13 - number) + 1
    offset = dist_from_top * 4 + 1 + SUITS.index(suit)
    return str(offset) + ".png"

def create_playing_card(suit, number):
    card = Card()
    card.suit = suit
    card.number = number
    card.front_face = get_file_name(suit, number)
    card.back_face = "b1fv.png"
    return card

def compare_color(card1, card2):
    if card1.suit == "hearts" or card1.suit == "diamonds":
        return card2.suit == "spades" or card2.suit == "clubs"

    if card1.suit == "spades" or card1.suit == "clubs":
        return card2.suit == "hearts" or card2.suit == "diamonds"

class Hearts(Game):
    """
    Solitaire is a simple one player game
    """

    def __init__(self):
        super(Hearts, self).__init__()
        self.current_turn = None
        self.hearts_broken = False
        self.played_two_of_clubs = False

    def set_up(self):
        import random

        # Create our deck of cards
        all_cards = [create_playing_card(x, y)
                 for x in SUITS for y in range(2, 15)]
        self.register(all_cards)

        random.shuffle(all_cards)

        # Deal out among the players
        while len(all_cards) >= len(self.players):
            for player in self.players:
                player.hand.push(all_cards.pop())

        # Set card owners
        for player in self.players:
            for card in player.hand.get_cards():
                if card.number == 2 and card.suit == 'clubs':
                    self.current_turn = player
                card.owner = player
                card.face_up = False
                card.set_value("face_up", True, player)

        # Set any extra cards to the side
        self.side_zone.set_cards(all_cards)
        if (self.current_turn is None):
            raise ValueError("2 of clubs was not in any hand")

        self.play_zone.suit = None

    def is_over(self):
        """
        Hearts is over if everybody has played all their cards
        """

        return (self.players[0].hand.get_num_cards() == 0)


    def winners(self):
        """
        Count up the number of cards in each player's discard zone.
        """

        def card_score(card):
            if card.suit == 'spades' and card.number == 12:
                return 13
            elif card.suit == 'hearts':
                return 1
            else:
                return 0

        min_score = float('inf')
        best_players = []
        for player in self.players:
            score = sum([card_score(x) for x in player.discard])
            if score < min_score:
                best_players = [player]
            elif score == min_score:
                best_players.append(player)

        return best_players


    def can_play_card(self, player, card):
        """
        Make sure that a player can play a card.
        """

        # Make sure we own the card an it's in our hand
        if card not in player.hand:
            return False

        # Make sure it's our turn.
        if self.current_turn != player:
            return False

        if (not self.played_two_of_clubs and
            not (card.number == 2 and card.suit == 'clubs')):
            return False

        # If everybody has already played then we can't play any more
        if self.play_zone.get_num_cards() == len(self.players):
            return False

        # Check the card suit (if it's not the leading suit and we have one)
        leading_suit = self.play_zone.suit

        if leading_suit is None:
            if card.suit == 'hearts' and not self.hearts_broken:
                return False
        else:
            if (leading_suit != card.suit and
                len([x for x in player.hand.get_cards() if x.suit == leading_suit]) > 0):
                return False

        return True

    def can_take_trick(self, player):

        print "Checking if you can take trick"
        if self.play_zone.get_num_cards() != len(self.players):
            return False

        print "There are enough cards in there."

        # Find the highest card
        valid_cards = [x for x in self.play_zone.get_cards()
                       if x.suit == self.play_zone.suit]
        max_card = None
        max_value = 0
        for card in valid_cards:
            if card.number > max_value:
                max_card = card
                max_value = card.number

        if max_card.owner != player:
            return False

        print "The maximum card is owned by the current player"

        return True


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

        self.play_zone.suit = None
        self.current_turn = player

        # Check if we need to take anything from the side_zone
        if self.side_zone.get_num_cards() > 0 and contains_point_card:
            while self.side_zone.get_num_cards() > 0:
                player.discard.push(self.size_zone.pop())


    def next_player(self, player):
        player_index = self.players.index(player)
        print self.players
        print player_index
        if player_index == (len(self.players) - 1):
            return self.players[0]
        else:
            return self.players[player_index + 1]
