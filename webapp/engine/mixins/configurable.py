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
        self.required_fields = set()
        # Optional values should be a dictionary of key to default value
        self.default_values = {}

    def load_config(self, config, ignore_keys=None):
        """
        First we make sure that all reuired values are present. If they are
        then we add all values. Otherwise, we throw a KeyError.
        """

        for required in self.required_fields:
            if required not in config:
                err = "Configuration missing field {0}".format(required)
                raise ValueError(err)

        # Load everything that we can out of the configuration
        for key in config:
            if ignore_keys is None or key not in ignore_keys:
                setattr(self, key, config[key])

        # Load up all optional vaule that haven't been accounted for
        for optional in self.default_values:
            if optional not in config:
                setattr(self, optional, self.default_values[optional])

        self.post_config_callback()

    def post_config_callback(self):
        """
        This can be overriden by subclasses that need to perform some kind
        of extra configuration after the configuration has been loaded.
        """

        pass
