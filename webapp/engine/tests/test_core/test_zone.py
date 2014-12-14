"""
This module contains all the code needed to test a Zone.
"""

from unittest import TestCase

from engine.core.game_object import GameObject
from engine.core.zone import Zone


class ZoneTestCase(TestCase):

    """
    Test the base zone class. Most of this pertains to the
    list like functionality.
    """

    def setUp(self):
        self.zone = Zone()
        self.object1 = GameObject()
        self.object2 = GameObject()
        self.subzone = {'name': 'subzone'}

        self.zone.game_id = 1
        self.object1.game_id = 2
        self.object2.game_id = 3

    def test_in(self):
        """
        Make sure we can use the 'in' operator on a zone.
        """

        self.assertNotIn(self.object1, self.zone)

        self.zone.add(self.object1)
        self.assertIn(self.object1, self.zone)

    def test_iteration(self):
        """
        Make sure we can iterate over all cards in a zone.
        This should include any cards in the subzones.
        """

        def count_items_using_for_loop(zone):
            count = 0
            for _ in zone:
                count += 1
            return count

        self.assertEqual(0, count_items_using_for_loop(self.zone))

        self.zone.add(self.object1)
        self.assertEqual(1, count_items_using_for_loop(self.zone))

    def test_len(self):
        """
        Make sure we can use the len function to count the number
        of objects in a zone and all subzones. Note that this won't
        count the number of subzones.
        """

        self.assertEqual(0, len(self.zone))

        self.zone.add(self.object1)
        self.assertEqual(1, len(self.zone))

    def test_remove(self):
        """
        Ensure that we can remove objects. Note that if an object
        is actually stored in one of my subzones it will be removed
        from there.
        """

        self.zone.add(self.object1)
        self.assertIn(self.object1, self.zone)
        self.zone.remove(self.object1)
        self.assertNotIn(self.object1, self.zone)

        # Test the silent failure
        self.zone.remove(self.object1)

    def test_push(self):
        """
        Make sure that when we push items ordering is perserved.
        """

        self.zone.push(self.object1)
        self.zone.push(self.object2)

        self.assertListEqual(self.zone.objects, [self.object1,
                                                 self.object2])

    def test_pop(self):
        """
        Make sure things pop off in the right order.
        """

        self.zone.push(self.object1)
        self.zone.push(self.object2)

        self.assertEqual(self.zone.pop(), self.object2)
        self.assertEqual(self.zone.pop(), self.object1)

        self.assertIsNone(self.zone.pop())

    def test_insert(self):
        """
        Make sure that when we can insert into a specific position
        of a zone.
        """

        self.zone.push(self.object1)
        self.zone.insert(self.object2, 0)

        self.assertEqual(self.zone.pop(), self.object1)
        self.assertEqual(self.zone.pop(), self.object2)

    def test_shuffle(self):
        """
        Make sure that we can shuffle a list and that it changes the
        results every time.
        """

        for _ in range(100):
            self.zone.push(GameObject())

        current = [x for x in self.zone.objects]

        self.zone.shuffle()
        self.assertNotEqual(current, self.zone.objects)

    def test_registers_transitions(self):
        """
        Make sure that when we add/remove cards that a transiton is registered
        with our game.
        """

        class MockGame(object):

            def __init__(self):
                self.transitions = []

            def add_transition(self, transition):
                self.transitions.append(transition)

            def get_and_pop_transition(self):
                return self.transitions.pop()

        mock_game = MockGame()
        self.zone.game = mock_game

        # Try adding a game object
        self.zone.add(self.object1)
        self.assertDictEqual(mock_game.get_and_pop_transition(),
                             {'name': 'add',
                              'object': self.object1.game_id,
                              'zone': self.zone.game_id})

        self.zone.remove(self.object1)
        self.assertDictEqual(mock_game.get_and_pop_transition(),
                             {'name': 'remove',
                              'object': self.object1.game_id,
                              'zone': self.zone.game_id})

        self.zone.push(self.object1)
        self.assertDictEqual(mock_game.get_and_pop_transition(),
                             {'name': 'add',
                              'object': self.object1.game_id,
                              'zone': self.zone.game_id})

        self.zone.pop()
        self.assertDictEqual(mock_game.get_and_pop_transition(),
                             {'name': 'remove',
                              'object': self.object1.game_id,
                              'zone': self.zone.game_id})
