class StepState(object):
    """
    This is basically a value container for the current
    state of the steps that are running in a game.
    """

    def __init__(self):
        self.global_state = {}
        self.current_state = {}

    def add_argument(self, name, value, add_global = False):
        if name is not None:
            if add_global == True:
                self.global_state[name] = value
            else:
                self.current_state[name] = value

    def start_step(self, args):
        if args is not  None:
            for key in args:
                self.current_state[key] = args[key]

    def get_kwargs(self):
        """
        Construct a list of keyword arguments. Note that local variables
        have precedence over global variables.
        """

        result = {}
        for key in self.global_state:
            result[key] = self.global_state[key]

        for key in self.current_state:
            result[key] = self.current_state[key]

        return result

    def finish_step(self):
        self.current_state = {}

    def flush(self):
        self.current_state = {}
