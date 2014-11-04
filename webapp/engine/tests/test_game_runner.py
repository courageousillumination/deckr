from unittest import TestCase, skip

import engine.game_runner


class GameRunnerTestCase(TestCase):

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
        game_id = engine.game_runner.create_game(self.valid_game_def)
        engine.game_runner.destroy_game(game_id)
        self.assertFalse(engine.game_runner.has_game(game_id))
        
    @skip("Not yet implemented")
    def test_get_state(self):
        state = engine.game_runner.get_state(self.game_id) 
        self.assertEqual(state, {}) # TODO: What is the expected state?
        
    @skip("Not yet implemented")
    def test_add_player(self):
        player_id = engine.game_runner.add_player(self.game_id)
        self.assertTrue(player_id > 0)
        self.assertNotEqual(player_id,
                            engine.game_runner.add_player(self.game_id))
        
    @skip("Not yet implemented")
    def test_make_action(self):
        game1 = engine.game_runner.get_game(self.game_id)
        game1.phase = "restricted"
        self.assertFalse(engine.game_runner.make_action("restricted_action"))
        game1.phase = "unrestricted"
        self.assertTrue(engine.game_runner.make_action("restricted_action"))

