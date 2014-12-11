"""
This file contains all logic around game steps. These have significantly more
logic than the simple actions and so have been pulled out into their own file.
"""

from engine.exceptions import NeedsMoreInfo


class StepState(object):
    """
    This class encapsulates the idea of state between steps. It basically
    wraps a dictionary, but offers some additional convience methods.
    """

    def __init__(self):
        self.state = {}



class Requirement(object):
    """
    A Requirement represents some variable that is needed by a game_step.
    At minimum this is a variable name and type. In addition to a type a
    container can be specified (the default is a singleton). There is also
    the option to add a test to make sure the variable is valid.

    NOTE: The only supported container is List or Singleton
    """

    def __init__(self, variable_name, variable_type,
                 variable_container = 'singleton', valid_test = None):
        self.variable_name = variable_name
        self.valid_test = valid_test
        self.variable_type = variable_type
        self.variable_container = variable_container

    def verify_kwargs(self, *args, **kwargs):
        """
        Takes in a dictionary of keyword arguments and makes sure everything
        checks out. Returns False if something is wrong (either the variable
        is not there or the validity test fails) and True otherwise.goo
        """

        value = kwargs.get(self.variable_name, None)
        if value is None:
            return False

        # Make sure that we check the container
        if self.variable_container == "list" and not isinstance(value, list):
            return False

        return self.valid_test(*args, **kwargs)
