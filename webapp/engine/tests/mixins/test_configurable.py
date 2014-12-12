"""
Contains any tests around the Configurable mixin
"""

from unittest import TestCase

from engine.mixins.configurable import Configurable


class MockConfigurable(Configurable):
    def __init__(self):
        super(MockConfigurable, self).__init__()
        self.callback_called = False

    def post_config_callback(self):
        self.callback_called = True

class ConfigurableTestCase(TestCase):
    def setUp(self):
        self.configurable = MockConfigurable()

    def test_load_configuration(self):
        """
        Make sure we can load up a simple configuration.
        """

        self.configurable.load_config({'foo': 'baz'})
        self.assertEqual(self.configurable.foo, 'baz')

    def test_required_fields(self):
        """
        Make sure that we can specify some fields as required and that the
        configuration throws an exception if those fields aren't present.
        """

        self.configurable.required_fields.add('foo')
        self.assertRaises(ValueError, self.configurable.load_config,
                          {'bar': 1})

        self.configurable.load_config({'foo': 'baz'})
        self.assertEqual(self.configurable.foo, 'baz')

    def test_default_values(self):
        """
        Make sure that we can specify default values for specific fields.
        """

        self.configurable.default_values['foo'] = 1
        self.configurable.load_config({'bar': 'baz'})

        self.assertEqual(self.configurable.foo, 1)
        self.assertEqual(self.configurable.bar, 'baz')

    def test_ignore_keys(self):
        """
        Make sure that we can ignore specific keys.
        """

        ignore_keys = ['ignore_me', 'ignore_me_too']
        self.configurable.load_config({'foo': 'bar',
                                       'ignore_me': 'secret',
                                       'ignore_me_too': 'top_secret'},
                                       ignore_keys = ignore_keys)

        self.assertEqual(self.configurable.foo, 'bar')
        self.assertFalse(hasattr(self.configurable, 'ignore_me'))
        self.assertFalse(hasattr(self.configurable, 'ignore_me_too'))

    def test_callback(self):
        """
        Make sure we call the postconfig callback.
        """

        self.configurable.load_config({})
        self.assertTrue(self.configurable.callback_called)
