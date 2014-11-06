"""
This module contains any tests around the GameRunner. This is a harder
class to test because it's stateful, so make sure you're careful about
that. Note that the game runner is a __module__ not a class (this is
the best way we could think of to implement the singleton pattern).
"""

from unittest import TestCase, skip

import engine.game_runner


class GameRunnerTestCase(TestCase):

    """
    A pretty straightforward test case for the GameRunner.
    """

    def setUp(self):
        self.valid_game_def = "engine/tests/data/simple_game"
        self.game_id = engine.game_runner.create_game(self.valid_game_def)

    def tearDown(self):
        engine.game_runner.flush()

    @skip("Not yet implemented")
    def test_create_room(self):
        """
        Test the ability to create a game room.
        """

        try:
            engine.game_runner.create_game("invalid file")
            self.fail()
        except IOError:
            pass

        game_id = engine.game_runner.create_game(self.valid_game_def)
        self.assertTrue(game_id > 0)

        # Make sure IDs are unique
        game_id_1 = engine.game_runner.create_game(self.valid_game_def)
        self.assertNotEqual(game_id, game_id_1)

    @skip("Not yet implemented")
    def test_destroy_room(self):
        """
        Make sure that we can destroy a game room.
        """

        game_id = engine.game_runner.create_game(self.valid_game_def)
        engine.game_runner.destroy_game(game_id)
        self.assertFalse(engine.game_runner.has_game(game_id))

    @skip("Not yet implemented")
    def test_get_state(self):
        """
        Makes sure we can get the state out of a game.
        """

        expected_state = {
            "zone1": {
                "id": 1,
                "cards": [{"id": 1}]
            }
        }

        game_id = engine.game_runner.create_game(self.valid_game_def)
        state = engine.game_runner.get_state(game_id)
        self.assertEqual(state, expected_state)

    @skip("Not yet implemented")
    def test_add_player(self):
        """
        Makes sure that we can add a player and get back a valid
        id.
        """

        player_id = engine.game_runner.add_player(self.game_id)
        self.assertTrue(player_id > 0)
        self.assertNotEqual(player_id,
                            engine.game_runner.add_player(self.game_id))

    @skip("Not yet implemented")
    def test_make_action(self):
        """
        Make sure that we can make actions through the GameRunner.
        """

        game1 = engine.game_runner.get_game(self.game_id)
        game1.phase = "restricted"
        self.assertFalse(engine.game_runner.make_action("restricted_action"))
        game1.phase = "unrestricted"
        self.assertTrue(engine.game_runner.make_action("restricted_action"))
