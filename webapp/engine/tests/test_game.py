from unittest import TestCase, skip

import engine.card

from engine.tests.mock_game import MockGame


class GameTestCase(TestCase):

    def setUp(self):
        self.game = MockGame()
        self.game.set_up()

    @skip("not yet implemented")
    def test_set_up(self):
        """
        Make sure that setup can't be called twice
        and that it was run on class creation.
        """

        self.assertTrue(self.game.is_setup)
        self.assertFalse(self.game.set_up())
        self.assertTrue(self.game.is_setup)

    @skip("not yet implemented")
    def test_assign_id(self):
        """
        Make sure that assigning IDs works.
        """

        card1 = engine.card.Card()

        self.assertTrue(self.game.assign_id(card1, 1))
        self.assertEqual(card1.get_id(), 1)

        self.assertFalse(self.game.assign_id(card1, 1))
        self.assertEqual(card1.get_id(), 1)

        self.assertFalse(self.game.assign_id(None, ""))

    @skip("not yet implemented")
    def test_make_action(self):
        """
        Make sure that restrictions work on making actions.
        """

        self.game.phase = "restricted"
        self.assertFalse(self.game.make_action("restricted_action",
                                               player_id=1))
        self.game.phase = "unrestricted"
        self.assertTrue(self.game.make_action("restricted_action",
                                              player_id=1))

    @skip("not yet implemented")
    def test_make_winning_action(self):
        """
        Make sure that we can win the game.
        """

        self.game.make_action("win", player_id=1)
        self.assertTrue(self.game.is_over())
        self.assertListEqual([1], self.game.winners())

    @skip("not yet implemented")
    def test_make_losing_action(self):
        """
        Make sure that we can lose the game.
        """

        self.game.make_action("lose", player_id=1)
        self.assertTrue(self.game.is_over())
        self.assertListEqual([], self.game.winners())
