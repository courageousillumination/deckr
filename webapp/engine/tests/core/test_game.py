"""
This module contains all test for the Game class.
"""

from unittest import TestCase

from engine.core.game import Game
from engine.core.game_object import GameObject
from engine.core.transition import Transition


class TestGameObject(GameObject):
    pass

class SimpleGame(Game):

    def __init__(self):
        super(SimpleGame, self).__init__()
        self.min_players = 1
        self.max_players = 1

    def set_up(self):
        pass

    def is_over(self):
        return False

    def winners(self):
        return []

class BaseGameTestCase(TestCase):
    """
    Test functionality provided by the base game. The tests in this test case
    should not depend on anything outside of the base game.
    """

    def setUp(self):
        self.game = Game()
        self.game.max_players = 2

    def test_registration(self):
        """
        Make sure that the game can register and deregister
        objects properly.
        """

        object1 = GameObject()
        object2 = "Foo" # Test with non game object.
        object_list = [GameObject(), GameObject()]

        self.game.register(object1)
        self.game.register(object2)
        self.game.register(object_list)

        self.assertEqual(1, object1.game_id)
        self.assertEqual(2, object_list[0].game_id)
        self.assertEqual(3, object_list[1].game_id)
        self.assertEqual(4, self.game.next_game_id)

        self.assertEqual(self.game, object1.game)
        self.assertEqual(self.game, object_list[0].game)
        self.assertEqual(self.game, object_list[1].game)

    def test_get_object(self):
        """
        Make sure we can get an object by the ID, specifying
        the class if necessary.
        """

        object1 = GameObject()
        object2 = GameObject()
        object3 = TestGameObject()

        self.game.register(object1)
        self.game.register(object2)
        self.game.register(object3)

        self.assertEqual(self.game.get_object_with_id(object1.game_id),
                         object1)
        self.assertEqual(self.game.get_object_with_id(object2.game_id),
                         object2)
        self.assertEqual(self.game.get_object_with_id(object3.game_id),
                         object3)

        fetched = self.game.get_object_with_id(object3.game_id,
                                               TestGameObject)
        self.assertEqual(fetched, object3)
        self.assertIsNone(self.game.get_object_with_id(-1))
        self.assertIsNone(self.game.get_object_with_id(object1.game_id,
                                                       TestGameObject))

    def test_deregister(self):
        """
        Make sure that we can remove an object, freeing it up for GC.
        """

        object1 = GameObject()
        object2 = GameObject()
        object3 = GameObject()
        non_game_object = "Foo"
        object_list = [object2, object3]
        all_objects = [object1, object2, object3]

        self.game.register(all_objects)
        # deregister
        self.game.deregister(object1)
        self.game.deregister(object_list)
        self.game.deregister(non_game_object)
        self.game.deregister(object1) # Double deregister

        self.assertIsNone(self.game.get_object_with_id(object1.game_id))
        self.assertIsNone(self.game.get_object_with_id(object2.game_id))
        self.assertIsNone(self.game.get_object_with_id(object3.game_id))

    def test_get_state(self):
        """
        Make sure that we can get the state of the current game (the state
        being a list of all registered objects and their attributes).
        """

        object1 = GameObject()
        object2 = GameObject()

        self.game.register(object1)
        self.game.register(object2)

        game_state = self.game.get_state(serialize = False)

        self.assertEqual(len(game_state), 3)
        self.assertIn(self.game, game_state)
        self.assertIn(object1, game_state)
        self.assertIn(object2, game_state)

    def test_transitions(self):
        """
        Make sure we can add and get transitions properly.
        """

        transition1 = Transition()
        transition2 = Transition()

        player1 = self.game.add_player()
        player2 = self.game.add_player()

        self.game.add_transition(transition1)
        self.game.add_transition(transition2, player1)

        self.assertEqual(self.game.get_transitions(player1, serialize = False),
                         [transition1, transition2])

        self.assertEqual(self.game.get_transitions(player2, serialize = False),
                         [transition1])

        self.assertEqual(self.game.get_transitions(player1, serialize = False),
                         [])
        self.assertEqual(self.game.get_transitions(player2, serialize = False),
                         [])

    def test_add_player(self):
        """
        Make sure that we can add players and that the proper validation
        kicks in.
        """

        player1 = self.game.add_player()
        player2 = self.game.add_player()

        self.assertEqual(len(self.game.players), 2)
        self.assertEqual(self.game.players[0].game_id, player1)
        self.assertEqual(self.game.players[1].game_id, player2)

        self.assertRaises(ValueError, self.game.add_player)

        self.game.max_players = 4
        self.game.is_set_up = True
        self.assertRaises(ValueError, self.game.add_player)

    def test_remove_player(self):
        """
        Make sure we can remove a player.
        """

        player = self.game.add_player()

        self.game.remove_player(player)

        self.assertIsNone(self.game.get_object_with_id(player))

        self.game.remove_player(player)

    def test_setup_wrapper(self):
        """
        Make sure that the setup wrapper prevents double set ups or other
        invalid configurations.
        """

        simple_game = SimpleGame()

        self.assertFalse(simple_game.set_up_wrapper())

        simple_game.add_player()

        self.assertTrue(simple_game.set_up_wrapper())
        self.assertFalse(simple_game.set_up_wrapper())

    def test_config(self):
        """
        Make sure that we have set up the game so that it is properly
        configurable.
        """

        # Need min players
        self.assertRaises(ValueError, self.game.load_config, {})
        # Need max players
        self.assertRaises(ValueError, self.game.load_config, {'min_players': 0})

        self.game.load_config({'min_players': 0,
                               'max_players': 0,
                               'game_zones': [{'name': 'test_zone'}]})

        # This will test that the zone exists and that it was properly
        # registered with the game.
        self.assertEqual(self.game, self.game.test_zone.game)


    def test_abstract_methods(self):
        """
        Make sure our methods are abstract (mainly for coverage)
        """

        self.assertRaises(NotImplementedError, self.game.set_up)
        self.assertRaises(NotImplementedError, self.game.is_over)
        self.assertRaises(NotImplementedError, self.game.winners)
