from unittest import TestCase, skip

from engine.zone import Zone
from engine.card import Card

class ZoneTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @skip("not yet implemented")
    def test_add_card(self):
        """
        Test adding cards to a Zone.
        """
        card1 = Card()
        card2 = Card()

        test_zone = Zone()
        
        test_zone.add_card(card1)
        self.assertIn(card1, test_zone.get_cards())

        test_zone.add_card(card2)
        self.assertIn(card2, test_zone.get_cards())

        # Make sure we have both
        self.assertListEqual([card1,card2], test_zone.get_cards())

    @skip("not yet implemented")
    def test_remove_card(self):
        """
        Test removing cards from a zone.
        """
        card1 = Card()
        card2 = Card()
        card3 = Card()

        test_zone = Zone()
        
        test_zone.add_card(card1)
        test_zone.add_card(card2)
        self.assertListEqual([card1,card2], test_zone.get_cards())
        
        # Check that the right card is removed, and only that card
        test_zone.remove_card(card1)

        self.assertNotIn(card1, test_zone.get_cards())
        self.assertIn(card2, test_zone.get_cards())

        # Cannot remove a card not in the list
        self.assertFalse(test_zone.remove_card(card3))

    @skip("not yet implemented")
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

    @skip("not yet implemented")
    def test_shuffle(self):
        """
        Test shuffling the cards.
        """
        test_zone = Zone()

        for x in range(0, 100):
            test_zone.add_card(Card())

        temp = test_zone.get_cards()[:]
        test_zone.shuffle()

        # Make sure cards were shuffled and that we didn't lose any
        self.assertListNotEqual(temp, test_zone.get_cards())
        self.assertEqual(len(temp),len(test_zone.get_cards()))

    @skip("not yet implemented")
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
        # Exact format not yet determined
        pass

    @skip("not yet implemented")
    def test_push(self):
        """
        Test pushing cards to our list.
        """
        card1 = Card()
        card2 = Card()
        card3 = Card()

        test_zone = Zone()

        test_zone.push(card1)
        test_zone.push(card3)
        test_zone.push(card2)

        self.assertListEqual([card2,card3,card1], test_zone.get_cards())

    @skip("not yet implemented")
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
        self.assertEqual(card2,test_zone.pop())

        # Make sure it is popped
        self.assertListEqual([card3,card1], test_zone.get_cards())

