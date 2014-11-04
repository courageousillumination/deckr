from unittest import TestCase, skip

import engine.game_runner
import engine.game
import engine.card


class GameTestCase(TestCase):
    # TODO: write these cases

    def setUp(self):
        self.game = engine.game.Game()

    def tearDown(self):
        pass

    @skip("not yet implemented")
    def test_set_up(self):
        self.assertFalse(self.game.is_set_up)
        self.assertTrue(self.game.set_up())
        self.assertFalse(self.game.set_up())
        self.assertTrue(self.game.is_set_up)

    @skip("not yet implemented")
    def test_end(self):
        self.assertTrue(self.game.end())
        self.assertFalse(self.game.end())

    @skip("not yet implemented")
    def test_assign_id(self):
        self.assertTrue(self.game.assign_id(engine.card.Card(), "1"))
        self.assertFalse(self.game.assign_id(engine.card.Card(), "1"))
        self.assertFalse(self.game.assign_id(None, ""))

    @skip("not yet implemented")
    def test_is_over(self):
        self.assertFalse(self.game.is_over())
        self.game.lose()
        self.assertTrue(self.game.is_over())

    @skip("not yet implemented")
    def test_make_action(self):
        self.game.phase = "restricted"
        self.assertFalse(self.game.make_action("restricted_action"))
        self.game.phase = "unrestricted"
        self.assertTrue(self.game.make_action("restricted_action"))
