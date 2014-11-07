"""
This module contains all the code needed to test a Zone.
"""

from unittest import TestCase, skip

from engine.zone import Zone
from engine.card import Card
from engine.game import Game


class ZoneTestCase(TestCase):

    """
    Simple test case around Zones.
    """

    def test_add_card(self):
        """
        Test adding cards to a Zone.
        """
        card1 = Card()
        card2 = Card()

        test_zone = Zone()

        test_zone.add_card(card1)
        self.assertIn(card1, test_zone.get_cards())

        # No null cards, no duplicates
        self.assertFalse(test_zone.add_card(None))
        self.assertFalse(test_zone.add_card(card1))

        self.assertListEqual([card1], test_zone.get_cards())

        test_zone.add_card(card2)
        self.assertIn(card2, test_zone.get_cards())

        # Make sure we have both
        self.assertListEqual([card1, card2], test_zone.get_cards())

    def test_remove_card(self):
        """
        Test removing cards from a zone.
        """
        card1 = Card()
        card2 = Card()
        card3 = Card()

        test_zone = Zone()

        # Cannot add null cards, but other stuff is fine
        test_zone.add_card(card1)
        test_zone.add_card(card2)

        self.assertListEqual([card1, card2], test_zone.get_cards())

        # Check that the right card is removed, and only that card
        test_zone.remove_card(card1)

        self.assertNotIn(card1, test_zone.get_cards())
        self.assertIn(card2, test_zone.get_cards())

        # Cannot remove a card not in the list
        self.assertFalse(test_zone.remove_card(card3))

    def test_contains(self):
        """
        Test checking if a card is in the zone.
        """

        card1 = Card()
        card2 = Card()

        test_zone = Zone()

        test_zone.add_card(card1)
        self.assertTrue(card1 in test_zone)
        self.assertFalse(card2 in test_zone)

    def test_shuffle(self):
        """
        Test shuffling the cards.
        """

        test_zone = Zone()

        for _ in range(0, 100):
            test_zone.add_card(Card())

        temp = test_zone.get_cards()[:]
        test_zone.shuffle()

        # Make sure cards were shuffled and that we didn't lose any
        self.assertFalse(temp == test_zone.get_cards())
        self.assertEqual(len(temp), len(test_zone.get_cards()))

    def test_get_num_cards(self):
        """
        Test getting the number of cards in the zone.
        """

        card1 = Card()
        card2 = Card()

        test_zone = Zone()

        test_zone.add_card(card1)
        test_zone.add_card(card2)

        self.assertEqual(2, test_zone.get_num_cards())

    @skip("not yet implemented")
    def test_get_info(self):
        """
        Test getting zone info.
        """

        expected = {"hidden": False, "orientation": 1}
        test_zone = Zone()
        self.assertDictEqual(expected, test_zone.get_info())

    def test_push(self):
        """
        Test pushing cards to our list.
        """

        card1 = Card()
        card2 = Card()
        card3 = Card()

        test_zone = Zone()

        # No duplicates
        self.assertTrue(test_zone.push(card1))
        self.assertFalse(test_zone.push(card1))

        self.assertTrue(test_zone.push(card3))
        self.assertTrue(test_zone.push(card2))

        # No null cards
        self.assertFalse(test_zone.push(None))

        self.assertListEqual([card1, card3, card2], test_zone.get_cards())

    def test_pop(self):
        """
        Test popping a card from our list.
        """

        card1 = Card()
        card2 = Card()
        card3 = Card()

        test_zone = Zone()

        test_zone.push(card1)
        test_zone.push(card3)
        test_zone.push(card2)

        # Make sure we pop the right card
        self.assertEqual(card2, test_zone.pop())

        # Make sure it is popped
        self.assertListEqual([card1, card3], test_zone.get_cards())

        self.assertEqual(card3, test_zone.pop())
        self.assertEqual(card1, test_zone.pop())

        # Try to pop when there are no cards left
        self.assertEqual(0, len(test_zone.get_cards()))
        self.assertEqual(None, test_zone.pop())

    def test_zone_change_registers_with_game(self):
        """
        Make sure that when we move/add/remove cards from a zone
        that the game picks up on it.
        """

        game = Game()

        test_zone = Zone()
        card1 = Card()

        game.register([test_zone, card1])

        expected_transitions = [("add",
                                 card1.game_id,
                                 test_zone.game_id)]

        expected_transitions2 = [("add",
                                  card1.game_id,
                                  test_zone.game_id),
                                 ("remove",
                                  card1.game_id)]

        # Test add card
        test_zone.add_card(card1)
        self.assertEqual(game.get_transitions(), expected_transitions)
        test_zone.remove_card(card1)
        game.flush_transitions()

        # Test push card
        test_zone.push(card1)
        self.assertEqual(game.get_transitions(), expected_transitions)
        test_zone.remove_card(card1)
        game.flush_transitions()

        # Test remove card
        test_zone.add_card(card1)
        test_zone.remove_card(card1)
        self.assertEqual(game.get_transitions(), expected_transitions2)
        game.flush_transitions()

        # Test pop card
        test_zone.push(card1)
        c = test_zone.pop()
        self.assertEqual(card1, c)
        self.assertEqual(game.get_transitions(), expected_transitions2)
        game.flush_transitions()

        # Make sure we don't get transitions if there's bad data
        test_zone.add_card(card1)
        test_zone.add_card(card1)
        self.assertEqual(game.get_transitions(), expected_transitions)
        test_zone.remove_card(card1)
        game.flush_transitions()

        test_zone.pop()
        test_zone.remove_card(card1)
        self.assertEqual(game.get_transitions(), [])
