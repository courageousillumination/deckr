"""
This module provides an implementation of a game of Solitaire
"""

from engine.game import Game, action
from engine.card import Card

SUITS = ["clubs", "spades", "hearts", "diamonds"]

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
    card.src = get_file_name(suit, number)
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
        """
        """
   
        # Create our deck of cards
        cards = [create_playing_card(x, y) for x in SUITS for y in range(1, 14)]
        self.register(cards)
        self.deck.set_cards(cards)
        self.deck.shuffle()
        for i in range(1, 8):
            zone = self.zones["play_zone"+str(i)]
            for j in range(0, i):
                zone.push(self.deck.pop())
            card = zone.peek()    
            card.face_up = True
            
        print self.registered_objects

    def is_over(self):
        """
        Just looks at the internal over variable.
        """

        for i in range(1, 5):
            if self.zones["victory_zone" + str(i)].get_num_cards() != 13:
                return False
        
        # TODO: Need to also check for losing here...
        
        return True

    def winners(self):
        """
        Returns the internal winners_list.
        """

        return []

    def move_card_restrictons(self, card, target_zone):
        
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

    def draw_restrictions(self):
        return (self.deck.get_num_cards() + 
                self.deck_flipped.get_num_cards()) > 0


    @action(restriction=move_card_restrictons)
    def move_cards(self, card, target_zone):
        """
        Move the top card from one zone to another.
        """
        
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
    def draw(self):
        
        if self.deck.get_num_cards() == 0:
            self.deck.set_cards(self.deck_flipped.get_cards())
            self.deck_flipped.set_cards([])
            for card in self.deck.get_cards():
                card.face_up = False
            
        card = self.deck.pop()
        card.face_up = True
        self.deck_flipped.push(card)
            