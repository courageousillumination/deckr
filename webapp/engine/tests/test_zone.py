from unittest import TestCase, skip

from engine.zone import Zone
from engine.card import Card

class ZoneTestCase(TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_add_card(self):
		card1 = Card()
		card2 = Card()

		test_zone = Zone()
		
		test_zone.add_card(card1)
		self.assertIn(card1, test_zone.get_cards())

		test_zone.add_card(card2)
		self.assertIn(card2, test_zone.get_cards())

	def test_remove_card(self):
		card1 = Card()
		card2 = Card()

		test_zone = Zone()
		
		test_zone.add_card(card1)
		test_zone.add_card(card2)
		self.assertListEqual([card1,card2], test_zone.get_cards())
		
		test_zone.remove_card(card1)

		self.assertNotIn(card1, test_zone.get_cards())
		self.assertIn(card2, test_zone.get_cards())

	def test_contains(self):
		card1 = Card()
		test_zone = Zone()
		
		test_zone.add_card(card1)
		self.assertTrue(card1 in test_zone)