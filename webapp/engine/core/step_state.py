"""
This module provides the StepState class.
"""


class StepState(object):

    """
    This is basically a value container for the current
    state of the steps that are running in a game. If using arguments are
    specified they will override any local arguments.
    """

    def __init__(self):
        self.global_state = {}
        self.current_state = {}

    def add_argument(self, name, value, add_global=False):
        """
        Add an argument to the current state. If the global flag is specified
        then this will be added to the global state. NOTE: If it is added to
        the global state, it is not automatically added to the local state.
        """

        if name is not None:
            if add_global == True:
                self.global_state[name] = value
            else:
                self.current_state[name] = value

    def start_step(self, args, using=None):
        """
        Starts the current state for a specific step. args should be a list
        of keyword arguments that should be included. using should be a
        dictionary mapping from local to global names.
        """

        if args is not None:
            for key in args:
                self.current_state[key] = args[key]

        if using is not None:
            for key, value in using.items():
                self.current_state[key] = self.global_state[value]

    def get_kwargs(self):
        """
        Construct a list of keyword arguments. Note that local variables
        have precedence over global variables.
        """

        result = {}

        for key in self.current_state:
            result[key] = self.current_state[key]

        return result

    def finish_step(self):
        """
        This should be called at the completion of every step. It will flush all
        the current state.
        """

        self.current_state = {}

    def flush(self):
        """
        This should be called when the step stack is exhausted. It will flush
        both global and local state.
        """

        self.current_state = {}
        self.global_state = {}
