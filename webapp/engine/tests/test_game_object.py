"""
Contains any tests around the base stateful game object.
"""

from unittest import TestCase

from engine.game_object import GameObject


class GameObjectTestCase(TestCase):

    """
    A simple test case for testing anything related to
    game objects that have important state.
    """

    def setUp(self):
        self.game_object = GameObject()
        self.game_object.game_id = 1

    def test_to_dict(self):
        """
        Make sure that a game object can be converted to a dict
        with GameObjects replaced by their game_id.
        """

        test_object = GameObject()
        test_object2 = GameObject()
        test_object.game_id = 10
        test_object2.game_id = 11

        self.game_object.foo = "bar"
        self.game_object.g1 = test_object
        self.game_object.g2 = [test_object, test_object2]

        self.assertDictEqual(self.game_object.to_dict(),
                             {"game_id": 1,
                              "foo": "bar",
                              "g1": test_object.game_id,
                              "g2": [test_object.game_id,
                                     test_object2.game_id]})

    def test_replace_game_objects(self):
        """
        Make sure that the GameObject has a method to replace iterables
        of GameObjects with their IDs.
        """

        test_object = GameObject()
        test_object2 = GameObject()
        test_object.game_id = 10
        test_object2.game_id = 11

        self.assertEqual(self.game_object.replace_game_objects(test_object),
                         test_object.game_id)

        # Make sure it works on lists
        test_list = self.game_object.replace_game_objects([test_object,
                                                           test_object2])
        self.assertListEqual(test_list,
                             [test_object.game_id, test_object2.game_id])

        # Make sure it works on nested lists
        nested_list = [[test_object], [[test_object2]]]
        expected_list = [[test_object.game_id], [[test_object2.game_id]]]
        test_list = self.game_object.replace_game_objects(nested_list)
        self.assertListEqual(test_list, expected_list)

        # Make sure it works on dictionaries
        test_dict = self.game_object.replace_game_objects({"foo": test_object})
        self.assertDictEqual(test_dict,
                             {"foo": test_object.game_id})
