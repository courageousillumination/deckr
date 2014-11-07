"""
This module contains all the code needed to test a Zone.
"""

from unittest import TestCase

from engine.zone import Zone
from engine.card import Card
from engine.game import Game


class ZoneTestCase(TestCase):

    """
    Simple test case around Zones.
    """

    def setUp(self):

        self.zone = Zone()
        self.card1 = Card()
        self.card2 = Card()
        self.card3 = Card()

    def test_add_card(self):
        """
        Test adding cards to a Zone.
        """

        self.zone.add_card(self.card1)
        self.assertIn(self.card1, self.zone.get_cards())

        # No null cards, no duplicates
        self.assertFalse(self.zone.add_card(None))
        self.assertFalse(self.zone.add_card(self.card1))

        self.assertListEqual([self.card1], self.zone.get_cards())

        self.zone.add_card(self.card2)
        self.assertIn(self.card2, self.zone.get_cards())

        # Make sure we have both
        self.assertListEqual([self.card1, self.card2],
                             self.zone.get_cards())

    def test_remove_card(self):
        """
        Test removing cards from a zone.
        """

        # Cannot add null cards, but other stuff is fine
        self.zone.add_card(self.card1)
        self.zone.add_card(self.card2)

        self.assertListEqual([self.card1, self.card2],
                             self.zone.get_cards())

        # Check that the right card is removed, and only that card
        self.zone.remove_card(self.card1)

        self.assertNotIn(self.card1, self.zone.get_cards())
        self.assertIn(self.card2, self.zone.get_cards())

        # Cannot remove a card not in the list
        self.assertFalse(self.zone.remove_card(self.card3))

    def test_contains(self):
        """
        Test checking if a card is in the zone.
        """

        self.zone.add_card(self.card1)
        self.assertTrue(self.card1 in self.zone)
        self.assertFalse(self.card2 in self.zone)

    def test_shuffle(self):
        """
        Test shuffling the cards.
        """

        for _ in range(0, 100):
            self.zone.add_card(Card())

        temp = self.zone.get_cards()[:]
        self.zone.shuffle()

        # Make sure cards were shuffled and that we didn't lose any
        self.assertFalse(temp == self.zone.get_cards())
        self.assertEqual(len(temp), len(self.zone.get_cards()))

    def test_get_num_cards(self):
        """
        Test getting the number of cards in the zone.
        """

        self.zone.add_card(self.card1)
        self.zone.add_card(self.card2)

        self.assertEqual(2, self.zone.get_num_cards())

    def test_get_info(self):
        """
        Test getting zone info.
        """

        expected = {"stacked": True}
        self.zone = Zone(stacked=True)
        self.assertDictEqual(expected, self.zone.get_info())

    def test_push(self):
        """
        Test pushing cards to our list.
        """

        # No duplicates
        self.assertTrue(self.zone.push(self.card1))
        self.assertFalse(self.zone.push(self.card1))

        self.assertTrue(self.zone.push(self.card3))
        self.assertTrue(self.zone.push(self.card2))

        # No null cards
        self.assertFalse(self.zone.push(None))

        self.assertListEqual([self.card1, self.card3, self.card2],
                             self.zone.get_cards())

    def test_pop(self):
        """
        Test popping a card from our list.
        """

        self.zone.push(self.card1)
        self.zone.push(self.card3)
        self.zone.push(self.card2)

        # Make sure we pop the right card
        self.assertEqual(self.card2, self.zone.pop())

        # Make sure it is popped
        self.assertListEqual([self.card1, self.card3],
                             self.zone.get_cards())

        self.assertEqual(self.card3, self.zone.pop())
        self.assertEqual(self.card1, self.zone.pop())

        # Try to pop when there are no cards left
        self.assertEqual(0, len(self.zone.get_cards()))
        self.assertEqual(None, self.zone.pop())

    def test_notify_game(self):
        """
        Make sure that when we move/add/remove cards from a zone
        that the game picks up on it.
        """

        game = Game()
        game.register([self.zone, self.card1])

        expected_transitions = [("add",
                                 self.card1.game_id,
                                 self.zone.game_id)]

        expected_transitions2 = [("add",
                                  self.card1.game_id,
                                  self.zone.game_id),
                                 ("remove",
                                  self.card1.game_id)]

        # Test add card
        self.zone.add_card(self.card1)
        self.assertEqual(game.get_transitions(), expected_transitions)
        self.zone.remove_card(self.card1)
        game.flush_transitions()

        # Test push card
        self.zone.push(self.card1)
        self.assertEqual(game.get_transitions(), expected_transitions)
        self.zone.remove_card(self.card1)
        game.flush_transitions()

        # Test remove card
        self.zone.add_card(self.card1)
        self.zone.remove_card(self.card1)
        self.assertEqual(game.get_transitions(), expected_transitions2)
        game.flush_transitions()

        # Test pop card
        self.zone.push(self.card1)
        card = self.zone.pop()
        self.assertEqual(self.card1, card)
        self.assertEqual(game.get_transitions(), expected_transitions2)
        game.flush_transitions()

        # Make sure we don't get transitions if there's bad data
        self.zone.add_card(self.card1)
        self.zone.add_card(self.card1)
        self.assertEqual(game.get_transitions(), expected_transitions)
        self.zone.remove_card(self.card1)
        game.flush_transitions()

        self.zone.pop()
        self.zone.remove_card(self.card1)
        self.assertEqual(game.get_transitions(), [])
