"""
This file contains all test cases for our execpitons.
"""

from unittest import TestCase

from engine.core.exceptions import InvalidMoveException, NeedsMoreInfo


class InvalidMoveExceptionTestCase(TestCase):

    def setUp(self):
        self.exception = InvalidMoveException("Invalid Move")

    def test_to_string(self):
        """
        Make sure that the string representation is correct.
        """

        self.assertEqual("Invalid Move", self.exception.__str__())


class NeedsMoreInfoTestCase(TestCase):

    def setUp(self):
        self.exception = NeedsMoreInfo(requirement='foo',
                                       message="Please input foo")

    def test_to_string(self):
        """
        Make sure that the string representation is correct.
        """

        self.assertEqual("Need more information for foo 'Please input foo'",
                         self.exception.__str__())
