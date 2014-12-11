"""
This file holds any exceptions that we create for the
game engine.
"""

class InvalidMoveException(Exception):

    """
    This will be raised whenever a player makes an invalid move.
    """

    def __init__(self, value=None):
        super(InvalidMoveException, self).__init__()
        self.value = value

    def __str__(self):
        return repr(self.value)


class NeedsMoreInfo(Exception):

    """
    This can be thrown by a step that needs more information before it can
    continue.
    """

    def __init__(self, requirement=None):
        super(NeedsMoreInfo, self).__init__()
        self.requirement = requirement

    def __str__(self):
        return "Need more information for {0}".format(self.requirement)
