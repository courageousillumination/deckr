"""
Contains any tests around the base stateful game object.
"""

from unittest import TestCase

from engine.core.game_object import GameObject


class GameObjectTestCase(TestCase):

    """
    A simple test case for testing anything related to
    game objects that have important state.
    """

    def setUp(self):
        self.game_object = GameObject()
        self.game_object.game_id = 1
        self.game_object.game_object_type = 'simple_object'

    def test_serialize_simple(self):
        """
        Make sure that we can properly serialize a simple game_object
        """

        self.game_object.bar = 10
        self.game_object.foo = 'foo'
        self.game_object.no_track = "don't track"
        self.game_object.game_attributes.add('foo')
        self.game_object.game_attributes.add('bar')

        serialized = self.game_object.serialize(None)
        self.assertDictEqual(serialized, {'game_id': 1,
                                          'game_object_type': 'simple_object',
                                          'foo': 'foo',
                                          'bar': 10})

    def test_serialize_nested(self):
        """
        Make sure that we can serialize a game object that has a
        nested game object.
        """

        subobject = GameObject()
        subobject.game_id = 2
        subobject.game_object_type = 'subobject'
        subobject.foo = 'foo'
        subobject.game_attributes.add('foo')

        self.game_object.subobject = subobject
        self.game_object.game_attributes.add('subobject')

        self.assertDictEqual(self.game_object.serialize(player_id=None,
                                                        full=True),
                             {'game_id': 1,
                              'game_object_type': 'simple_object',
                              'subobject': {
                                  'game_id': 2,
                                  'game_object_type': 'subobject',
                                  'foo': 'foo'
                              }})

        self.assertDictEqual(self.game_object.serialize(player_id=None,
                                                        full=False),
                             {'game_id': 1,
                              'game_object_type': 'simple_object',
                              'subobject': {
                                  'game_id': 2,
                                  'game_object_type': 'subobject'
                              }})

    def test_serialize_containers(self):
        """
        Make sure we can serialize a list of game objects and
        a dictionary of game objects.
        """

        object1 = GameObject()
        object2 = GameObject()

        object1.game_id = 2
        object2.game_id = 3
        object1.game_object_type = 'sample_object'
        object2.game_object_type = 'sample_object'

        object_list = [object1, object2]

        self.game_object.objects = object_list
        self.game_object.game_attributes.add('objects')

        self.assertDictEqual(self.game_object.serialize(player_id=None,
                                                        full=True),
                             {'game_id': 1,
                              'game_object_type': 'simple_object',
                              'objects': [{
                                  'game_id': 2,
                                  'game_object_type': 'sample_object'
                              },
                                  {
                                  'game_id': 3,
                                  'game_object_type': 'sample_object'
                              }]})

        object_dict = {'foo': object1, 'bar': object2}
        self.game_object.objects = object_dict

        self.assertDictEqual(self.game_object.serialize(player_id=None,
                                                        full=True),
                             {'game_id': 1,
                              'game_object_type': 'simple_object',
                              'objects': {'foo': {
                                  'game_id': 2,
                                  'game_object_type': 'sample_object'
                              },
                                  'bar': {
                                  'game_id': 3,
                                  'game_object_type': 'sample_object'
                              }}})

    def test_set_attribute(self):
        """
        Make sure that when we set game attributes the proper transitions
        are added.
        """

        class MockGame(object):

            def __init__(self):
                self.transitions = []

            def add_transition(self, transition, player_id=None):
                self.transitions.append(transition)

        mock_game = MockGame()
        self.game_object.game = mock_game
        self.game_object.game_attributes.add('foo')

        self.game_object.foo = 'baz'
        self.game_object.no_track = 'bar'
        self.assertEqual(len(mock_game.transitions), 1)

        self.assertDictEqual(mock_game.transitions[0],
                             {'name': 'set', 'class': 'simple_object',
                              'game_id': self.game_object.game_id,
                              'attribute': 'foo', 'value': 'baz'})

    def test_player_overrides(self):
        """
        Make sure that player overrides work as we exepect them to.
        """

        player1 = GameObject()
        player1.game_id = 1
        player2 = GameObject()
        player2.game_id = 2

        self.game_object.foo = 'bar'
        self.game_object.set_player_override('foo', 'baz', player1)

        self.assertEqual(self.game_object.get_value_for_player_id('foo', 1),
                         'baz')
        self.assertEqual(self.game_object.get_value_for_player_id('foo', 2),
                         'bar')
        self.assertIsNone(
            self.game_object.get_value_for_player_id(
                'bar',
                None))
