"""
Unit tests for deckr.
"""

from django.test import TestCase


class SimpleTestCase(TestCase):

    """
    Nothing to see here...
    """

    def test_addition(self):
        """
        Really just to check that the ALU still works.
        """

        self.assertEqual(1 + 1, 2)
