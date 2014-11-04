from unittest import TestCase, skip

import engine.game_runner
import engine.game

class GameTestCase(TestCase):
	#TODO: write these cases
	def setUp(self):
		pass

	def tearDown(self):
		pass

	@skip("not yet implemented")
	def test_set_up(self):
		self.assertTrue(engine.game.set_up())
		self.assertFalse(engine.game.set_up())

	@skip("not yet implemented")
	def test_end(self):
		self.assertTrue(engine.game.end())
		self.assertFalse(engine.game.end())

	@skip("not yet implemented")
	def test_assign_id(self):
		pass

	@skip("not yet implemented")
	def test_is_over():
		self.assertFalse(engine.game.is_over())

	@skip("not yet implemented")
	def test_make_action(self):
		pass