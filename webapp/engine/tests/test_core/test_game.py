"""
This module contains all test for the Game class.
"""

from unittest import TestCase

from engine.core.decorators import game_action, game_step
from engine.core.exceptions import InvalidMoveException
from engine.core.game import Game
from engine.core.game_object import GameObject
from engine.core.player import Player


class TestGameObject(GameObject):
    pass


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
        object2 = "Foo"  # Test with non game object.
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
        self.game.deregister(object1)  # Double deregister

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

        game_state = self.game.get_state(serialize=False)

        self.assertEqual(len(game_state), 3)
        self.assertIn(self.game, game_state)
        self.assertIn(object1, game_state)
        self.assertIn(object2, game_state)

    def test_transitions(self):
        """
        Make sure we can add and get transitions properly.
        """

        transition1 = {'name': 'foo'}
        transition2 = {'name': 'bar'}

        player1 = self.game.add_player()
        player2 = self.game.add_player()

        self.game.add_transition(transition1)
        self.game.add_transition(transition2, player1)

        self.assertEqual(self.game.get_transitions(player1, serialize=False),
                         [transition1, transition2])

        self.assertEqual(self.game.get_transitions(player2, serialize=False),
                         [transition1])

        self.assertEqual(self.game.get_transitions(player1, serialize=False),
                         [])
        self.assertEqual(self.game.get_transitions(player2, serialize=False),
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

    def test_config(self):
        """
        Make sure that we have set up the game so that it is properly
        configurable.
        """

        # Need min players
        self.assertRaises(ValueError, self.game.load_config, {})
        # Need max players
        self.assertRaises(
            ValueError, self.game.load_config, {
                'min_players': 0})

        self.game.load_config({'min_players': 0,
                               'max_players': 0,
                               'game_zones': [{'name': 'test_zone'}]})

        # This will test that the zone exists and that it was properly
        # registered with the game.
        self.assertEqual(self.game, self.game.test_zone.game)

    def test_add_step(self):
        """
        Make sure that we can add a step on both sides.
        """

        self.game.add_step(player=1, step='foo')
        self.assertEqual(self.game.steps[0], {'player': 1, 'step': 'foo',
                                              'save_as': None, 'args': None,
                                              'using': None})
        self.game.add_step(player=2, step='bar', prepend=True)
        self.assertEqual(self.game.steps[0], {'player': 2, 'step': 'bar',
                                              'save_as': None, 'args': None,
                                              'using': None})

    def test_requires_info(self):
        """
        Make sure that we can set and get the required_info.
        """

        player = GameObject()
        player.game_id = 1

        self.assertIsNone(self.game.get_requires_information())
        self.game.set_requires_information(player,
                                           {'name': 'foo', 'type': GameObject})
        self.assertDictEqual(self.game.get_requires_information(),
                             {'name': 'foo', 'type': 'GameObject', 'player': 1})
        self.game.set_requires_information(player,
                                           {'name': 'foo', 'type': str})
        self.assertDictEqual(self.game.get_requires_information(),
                             {'name': 'foo', 'type': 'str', 'player': 1})

    def test_send_information(self):
        """
        Make sure that we can send information and that the type is properly
        set.
        """

        object1 = GameObject()
        player = self.game.add_player()
        self.game.register(object1)

        self.game.set_requires_information(self.game.get_object_with_id(player),
                                           {'name': 'foo', 'type': GameObject})

        self.game.send_information(player, foo=object1.game_id)
        self.assertEqual(self.game.step_state.current_state['foo'],
                         object1)

        self.game.set_requires_information(self.game.get_object_with_id(player),
                                           {'name': 'foo', 'type': int})
        self.game.send_information(player, foo=1)
        self.assertEqual(self.game.step_state.current_state['foo'], 1)

    def test_abstract_methods(self):
        """
        Make sure our methods are abstract (mainly for coverage)
        """

        self.assertRaises(NotImplementedError, self.game.set_up)
        self.assertRaises(NotImplementedError, self.game.is_over)
        self.assertRaises(NotImplementedError, self.game.winners)

# After this point we have code that tests a very simple game. This is to
# test and make sure that actions, etc. all work as expected.


class SimpleGame(Game):

    # pylint: disable=unused-argument
    def __init__(self):
        super(SimpleGame, self).__init__()
        self.min_players = 1
        self.max_players = 2
        self.result = None
        self.restricted = True
        self.game_over = False

    def set_up(self):
        pass

    def is_over(self):
        return self.game_over

    def winners(self):
        return []

    @game_action(parameter_types=None, restriction=None)
    def simple_action(self, player):
        self.result = True

    @game_action(parameter_types=None,
                 restriction=lambda self, player: not self.restricted)
    def restricted_action(self, player):
        self.result = True

    @game_action(restriction=None,
                 parameter_types=[{'name': 'player1'}])
    def paramter_types_action(self, player, player1):
        self.result = player1

    @game_action(parameter_types=None, restriction=None)
    def end_game(self, player):
        self.game_over = True

    #################
    # Testing steps #
    #################

    @game_action(parameter_types=None, restriction=None)
    def simple_step_action(self, player):
        self.add_step(player=player,
                      step=self.simple_step)

    @game_step(requires=None)
    def simple_step(self, player):
        self.result = True

    @game_action(parameter_types=None, restriction=None)
    def requires_more_step_action(self, player, extra_args=None):
        self.add_step(player=player,
                      step=self.requires_more_step,
                      args=extra_args)

    @game_step(requires=[{'name': 'foo', 'type': Player}])
    def requires_more_step(self, player, foo):
        self.result = foo

    @game_action(parameter_types=None, restriction=None)
    def pass_through_step_action(self, player):
        self.add_step(player=player,
                      step=self.pass_through_step1,
                      save_as='step1_result')
        self.add_step(player=player,
                      step=self.pass_through_step2,
                      using={'foo': 'step1_result'})

    @game_step(requires=None)
    def pass_through_step1(self, player):
        return 'bar'

    @game_step(requires=[{'name': 'foo', 'type': str}])
    def pass_through_step2(self, player, foo):
        self.result = foo

    @game_action(restriction=None, parameter_types=None)
    def noop_action(self, player):
        self.add_step(player=player,
                      step=self.noop)

    @game_step(requires=None)
    def noop(self, player):
        pass

    ############
    # Triggers #
    ############

    def trigger1(self, player, **kwargs):
        self.result = 'triggered'


class SimpleGameTestCase(TestCase):

    def setUp(self):
        self.game = SimpleGame()
        self.player_id = self.game.add_player()

    def test_setup_wrapper(self):
        """
        Make sure that the setup wrapper prevents double set ups or other
        invalid configurations (not enough players)
        """

        self.game.min_players = 2
        self.assertFalse(self.game.set_up_wrapper())
        self.game.add_player()
        self.assertTrue(self.game.set_up_wrapper())
        self.assertFalse(self.game.set_up_wrapper())

    def test_simple_action(self):
        """
        Make sure that we can run a simple action.
        """

        self.game.make_action('simple_action', self.player_id)
        self.assertTrue(self.game.result)

    def test_restricted_action(self):
        """
        Make sure we can run a restricted action, and that things break
        properly if the action is invalid.
        """

        self.assertRaises(InvalidMoveException, self.game.make_action,
                          'restricted_action', self.player_id)

        self.game.restricted = False
        self.game.make_action('restricted_action', self.player_id)
        self.assertTrue(self.game.result)

    def test_parameter_correction(self):
        """
        Make sure that we can properly get objects from their ids using
        the parameter_types list.
        """

        self.assertRaises(InvalidMoveException, self.game.make_action,
                          'paramter_types_action', self.player_id,
                          player1=-1)

        self.game.make_action('paramter_types_action',
                              self.player_id, player1=self.player_id)

        self.assertTrue(isinstance(self.game.result, Player))
        self.assertEqual(self.game.players[0], self.game.result)

    def test_game_ending_action(self):
        """
        Make sure that we pick up the fact that the game is over.
        """

        self.game.make_action('end_game', self.player_id)
        self.assertDictEqual(self.game.transitions[self.player_id][0],
                             {'name': 'is_over', 'winners': []})

    def test_simple_step(self):
        """
        Make sure that we can add simple steps to the game.
        """

        self.game.make_action('simple_step_action', self.player_id)
        self.assertTrue(self.game.result)

    def test_step_requires_more(self):
        """
        Make sure that if a step requires more information then we are
        properly prompted and that, upon sending more information, the step
        proceeds.
        """

        self.game.make_action('requires_more_step_action', self.player_id)

        self.assertEqual(self.game.get_requires_information(),
                         {'name': 'foo', 'type': 'Player',
                          'player': self.player_id})
        self.assertIsNone(self.game.result)

        self.game.make_action('send_information', self.player_id, foo=1)
        self.assertEqual(self.game.result, self.game.players[0])

    def test_specify_args(self):
        """
        Make sure that we can explicitly pass in arguments.
        """

        self.game.make_action('requires_more_step_action', self.player_id,
                              extra_args={'foo': self.game.players[0]})
        self.assertEqual(self.game.result, self.game.players[0])

    def test_pass_through_step(self):
        """
        Make sure that we can pass from one step to another.
        """

        self.game.make_action('pass_through_step_action', self.player_id)
        self.assertEqual(self.game.result, 'bar')

    def test_add_and_remove_trigger(self):
        """
        Make sure we can add and remove triggers from specific steps.
        """

        self.game.add_trigger(self.game.simple_step, self.game.trigger1)
        self.assertEqual(self.game.pre_triggers['simple_step'],
                         [self.game.trigger1])
        self.game.remove_trigger(self.game.simple_step, self.game.trigger1)
        self.assertEqual(self.game.pre_triggers['simple_step'], [])

        self.game.add_trigger(self.game.simple_step, self.game.trigger1, True)
        self.assertEqual(self.game.post_triggers['simple_step'],
                         [self.game.trigger1])
        self.game.remove_trigger(self.game.simple_step, self.game.trigger1)
        self.assertEqual(self.game.post_triggers['simple_step'], [])

    def test_pre_triggers(self):
        """
        Make sure that triggers actually work.
        """

        self.game.add_trigger(self.game.noop, self.game.trigger1)
        self.game.make_action('noop_action', self.player_id)
        self.assertEqual(self.game.result, 'triggered')

    def test_post_triggers(self):
        """
        Make sure that we can add triggers after the step.
        """

        self.game.add_trigger(self.game.simple_step, self.game.trigger1,
                              post=True)
        self.game.make_action('simple_step_action', self.player_id)
        self.assertEqual(self.game.result, 'triggered')
