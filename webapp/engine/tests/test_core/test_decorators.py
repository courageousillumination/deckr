"""
Test all of the decorators provided by the game engine.
"""

from unittest import TestCase

from engine.core.decorators import game_serialize, game_step
from engine.core.exceptions import NeedsMoreInfo
from engine.core.game_object import GameObject


class GameSerializeTestCase(TestCase):

    """
    Test the various functionality of the game serialze method.
    """

    def test_no_seralize(self):
        """
        Make sure that we can use the game_serialize without interfering
        with a normal return type.
        """

        @game_serialize
        def simple():
            return 'foo'

        self.assertEqual('foo', simple())
        self.assertEqual('foo', simple(serialize=False))
        self.assertEqual('foo', simple(serialize=True))

    def test_serialize_single(self):
        """
        Make sure that if we're returning a single game object then
        it will be properly serialized.
        """

        @game_serialize
        def return_game_object():
            result = GameObject()
            result.game_id = 1
            result.game_object_type = 'simple_object'
            return result

        self.assertTrue(isinstance(return_game_object(serialize=False),
                                   GameObject))
        self.assertDictEqual(return_game_object(serialize=True),
                             {'game_id': 1,
                              'game_object_type': 'simple_object'})

    def test_serialize_list(self):
        """
        Make sure that if we're returning a single game object then
        it will be properly serialized.
        """

        @game_serialize
        def return_game_objects():
            result = GameObject()
            result.game_id = 1
            result.game_object_type = 'simple_object'
            return [result, 'bar']

        self.assertEqual(return_game_objects(serialize=True),
                         [{'game_id': 1,
                           'game_object_type': 'simple_object'}, 'bar'])

    def test_serialize_dict(self):
        """
        Make sure that if we're returning a single game object then
        it will be properly serialized.
        """

        @game_serialize
        def return_game_object():
            result = GameObject()
            result.game_id = 1
            result.game_object_type = 'simple_object'
            return {'foo': result, 'bar': 'baz'}

        self.assertDictEqual(return_game_object(serialize=True),
                             {'foo': {'game_id': 1,
                                      'game_object_type': 'simple_object'},
                              'bar': 'baz'})


class GameStepTestCase(TestCase):

    def test_requirement_list(self):
        """
        Make sure that we can require a list.
        """

        @game_step(requires=[{'name': 'foo', 'type': str,
                              'container': 'list'}])
        def requires_list(foo):
            return True

        self.assertRaises(NeedsMoreInfo, requires_list, foo='foo')
        self.assertRaises(NeedsMoreInfo, requires_list, foo=['foo', 1])
        self.assertTrue(requires_list(foo=['foo']))

    def test_requirement_improper_type(self):
        """
        Make sure that we do type checking on the requirements.
        """

        @game_step(requires=[{'name': 'foo', 'type': str}])
        def requires_string(foo):
            return True

        self.assertRaises(NeedsMoreInfo, requires_string, foo=1)
        self.assertTrue(requires_string(foo='foo'))

    def test_requirement_with_test(self):
        """
        Make sure that the test runs.
        """

        def simple_test(foo):
            return foo == 'foo'

        @game_step(requires=[{'name': 'foo', 'type': str,
                              'test': simple_test}])
        def step_with_test(foo):
            return True

        self.assertRaises(NeedsMoreInfo, step_with_test, foo='bar')
        self.assertTrue(step_with_test(foo='foo'))
