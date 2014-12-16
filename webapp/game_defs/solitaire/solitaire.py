"""
This module provides an implementation of a game of Solitaire
"""

from engine.core.decorators import game_action
from engine.core.game import Game
from engine.core.game_object import GameObject

SUITS = ["clubs", "spades", "hearts", "diamonds"]



class Card(GameObject):

    def __init__(self):
        super(Card, self).__init__()

        self.game_object_type = 'Card'
        self.front_face = None
        self.back_face = None
        self.face_up = False
        self.game_attributes.add('front_face')
        self.game_attributes.add('back_face')
        self.game_attributes.add('face_up')

def get_file_name(suit, number):
    if number == 1:
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

class Solitaire(Game):
    """
    Solitaire is a simple one player game
    """

    def set_up(self):
        # Create our deck of cards
        import random
        cards = [create_playing_card(x, y) for x in SUITS for y in range(1, 14)]
        self.register(cards)
        random.shuffle(cards)

        for card in cards:
            self.deck.push(card)

        for i in range(1, 8):
            zone = self.zones["play_zone"+str(i)]
            for _ in range(0, i):
                zone.push(self.deck.pop())
            zone.objects[-1].face_up = True

    def is_over(self):
        pass

    def winners(self):
        pass

    @game_action(restriction = None)
    def draw(self, player):
        card = self.deck.pop()
        card.face_up = True
        self.deck_flipped.push(card)

    """@game_action(restriction=None)
    def move_cards(self, player, card, target_zone):
        source_zone = card.zone
        # Pull all of the cards below the selected card.
        popped_card = None
        cards = []
        while popped_card != card:
            popped_card = source_zone.pop()
            cards.append(popped_card)

        for _ in range(len(cards)):
            target_zone.push(cards.pop())


        source_zone = card.zone
        popped_card = None
        cards = []
        while popped_card != card:
            popped_card = source_zone.pop()
            cards.append(popped_card)

        for i in range(len(cards)):
            target_zone.push(cards.pop())

        last_card = source_zone.peek()
        if last_card is not None and last_card.face_up == False:
            last_card.face_up = True
        """

    #def move_card_restrictons(self, player, card, target_zone):
    """
        Requires the following:
            1) The card is face up.
            2)
        if card.zone.zone_type == "victory" or card.face_up == False:
            return False
        elif (target_zone.zone_type == "victory"):
            return self.victory_zone_restrictions(card, target_zone)
        elif (target_zone.zone_type == "play"):
            return self.play_zone_restrictions(card, target_zone)
        else:
            return False

    def victory_zone_restrictions(self, card, target_zone):

        card_b = target_zone.peek()

        if card_b is None:
            return card.number == 1

        return card_b.suit == card.suit and card_b.number == card.number - 1

    def play_zone_restrictions(self, card, target_zone):

        card_b = target_zone.peek()

        if card_b is None:
            return card.number == 13

        return compare_color(card, card_b) and card_b.number == card.number + 1

    def draw_restrictions(self, player):
        return (self.deck.get_num_cards() +
                self.deck_flipped.get_num_cards()) > 0


    @action(restriction=move_card_restrictons)
    def move_cards(self, player, card, target_zone):


        source_zone = card.zone

        popped_card = None
        cards = []
        while popped_card != card:
            popped_card = source_zone.pop()
            cards.append(popped_card)

        for i in range(len(cards)):
            target_zone.push(cards.pop())

        last_card = source_zone.peek()
        if last_card is not None and last_card.face_up == False:
            last_card.face_up = True

    @action(restriction=draw_restrictions)
    def draw(self, player):

        if self.deck.get_num_cards() == 0:
            self.deck.set_cards(self.deck_flipped.get_cards())
            self.deck_flipped.set_cards([])
            for card in self.deck.get_cards():
                card.face_up = False

        card = self.deck.pop()
        card.face_up = True
        self.deck_flipped.push(card)
    """
