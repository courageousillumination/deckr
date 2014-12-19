"""
Contains any tests around card sets
"""

from unittest import TestCase

from engine.card_game.playing_card import create_deck, PlayingCard


class PlayingCardUtilTestCase(TestCase):
    """
    Test all utilities for playing cards.
    """

    def test_create_deck(self):
        """
        Make sure we can create a deck.
        """

        deck = create_deck()
        self.assertEqual(len(deck), 52)

class PlayingCardTestCase(TestCase):

    """
    This tests playing cards and all the functionality related to them.
    """

    def test_get_file_name(self):
        """
        Make sure that we can get the proper file name given a suit and number
        """

        ace = PlayingCard('clubs', 1)
        two = PlayingCard('spades', 2)

        self.assertEqual(ace.get_file_name(), '1.png')
        self.assertEqual(two.get_file_name(), '50.png')

    def test_get_color(self):
        """
        Make sure we can get the suit color.
        """

        clubs = PlayingCard('clubs', 1)
        spades = PlayingCard('spades', 1)
        hearts = PlayingCard('hearts', 1)
        diamonds = PlayingCard('diamonds', 1)

        self.assertEqual(clubs.get_color(), 'black')
        self.assertEqual(spades.get_color(), 'black')
        self.assertEqual(hearts.get_color(), 'red')
        self.assertEqual(diamonds.get_color(), 'red')
