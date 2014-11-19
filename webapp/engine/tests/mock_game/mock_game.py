"""
This module provides a very simple MockGame for testing. It has basic actions,
setup, and game ending conditions.
"""

from engine.game import Game, action
from engine.card import Card
from engine.zone import Zone
from engine.player import Player


class MockGame(Game):

    """
    The MockGame is basically the simplest game you could imagine.
    """

    def __init__(self):
        super(MockGame, self).__init__()

        self.winners_list = []
        self.over = False
        self.is_setup = False
        self.phase = None
        self.magic = 0x1337  # This is for Debugging.

    def set_up(self):
        """
        Just set the setup variable, and make sure the phase
        is restricted.
        """
        self.is_setup = True
        self.phase = "restricted"

    def is_over(self):
        """
        Just looks at the internal over variable.
        """

        return self.over

    def winners(self):
        """
        Returns the internal winners_list.
        """

        return [x.game_id for x in self.winners_list]

    def restrictions(self, player_id):  # pylint: disable=W0613
        """
        A simple restriction.
        """

        return self.phase != "restricted"

    @action(restriction=None)
    def win(self, player_id):
        """
        If we make this action we win the game.
        """

        self.winners_list.append(player_id)
        self.over = True

    @action(restriction=None)
    def lose(self, player_id):  # pylint: disable=W0613
        """
        If we make this action then we lose.
        """

        self.over = True

    @action(restriction=restrictions)
    def restricted_action(self, player_id):
        """
        This will win, if the phase isn't restricted.
        """

        self.winners_list.append(player_id)
        self.over = True

    @action(restriction=None)
    def test_argument_types(self, card, zone, player):
        """
        This makes sure that all the arguments have the
        right type.
        """

        assert isinstance(card, Card)
        assert isinstance(zone, Zone)
        assert isinstance(player, Player)

    @action(restriction=None)
    def private_public_action(self, player):
        """
        Make sure that we can add both public transitions and per player
        transitions.
        """

        self.add_transition(("public", "foobar"))
        self.add_transition(("private", "foobaz"), player)

    def get_magic(self):
        """
        This is just because isinstance of is acting poorly.
        """

        return self.magic
