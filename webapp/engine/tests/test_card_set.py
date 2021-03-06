"""
Contains any tests around card sets
"""

from unittest import TestCase

from engine.card import Card
from engine.card_set import CardSet


class CardSetTestCase(TestCase):

    """
    This tests card sets.
    """

    def setUp(self):
        self.card_set = CardSet()

        config = [
            {"name": "Copper",
             "cost": 1},
            {"name": "Silver",
             "cost": 2}
        ]

        self.card_set.load_from_list(config)

    def test_load_from_config(self):
        """
        Make sure that we can load a CardSet from a dictonary.
        """

        self.assertEqual(len(self.card_set.all_cards()), 2)

    def test_create_instances(self):
        """
        Make sure we can create instances using a CardSet.
        """

        # Make sure that we can create singletons
        silver = self.card_set.create("Silver")
        self.assertIsInstance(silver, Card)
        self.assertEqual(silver.cost, 2)

        # Make sure we can get multiple copies of a card
        coppers = self.card_set.create("Copper", 10)
        self.assertEqual(len(coppers), 10)
        self.assertIsInstance(coppers[0], Card)
        self.assertEqual(coppers[0].cost, 1)

        # Make sure that we can get a copy of every card
        card_instances = self.card_set.create_set()
        self.assertEqual(len(card_instances), 2)

        # Make sure no error is thrown if we try to create a non-positive number
        # of cards
        no_cards = self.card_set.create("Silver", -1)
        self.assertEqual(no_cards, [])

        # Make sure an error is thrown if we create a card that doesn't exist
        self.assertRaises(ValueError, self.card_set.create, "Gold")
