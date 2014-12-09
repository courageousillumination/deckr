"""
This file provides the configurable mixin.
"""

class Configurable(object):
    """
    A configurable object can take in a configuration
    (in the form of a dictionary) and perform some
    operations to load that configuration.
    """

    def __init__(self):
        super(Configurable, self).__init__()

        # These values are required and will throw an exception if the value
        # is missing.
        self.required_values = set()
        # Optional values should be a dictionary of key to default value
        self.optional_values = {}

    def load_from_config(self, config):
        """
        First we make sure that all reuired values are present. If they are
        then we add all values. Otherwise, we throw a KeyError.
        """

        for required in self.required_values:
            if required not in config:
                raise KeyError

        # Load everything that we can out of the configuration
        for key in config:
            setattr(self, key, config[key])

        # Load up all optional vaule that haven't been accounted for
        for optional in self.optional_values:
            if optional not in config:
                setattr(self, optional, self.optional_values[optional])
