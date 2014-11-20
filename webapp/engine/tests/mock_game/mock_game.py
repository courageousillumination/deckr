"""
This module provides a very simple MockGame for testing. It has basic actions,
setup, and game ending conditions.
"""

from engine.card import Card
from engine.game import action, Game, game_step
from engine.player import Player
from engine.zone import Zone


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

    # pylint: disable=unused-argument
    @action(restriction=None)
    def test_multi_step(self, **kwargs):
        """
        Test a simple multistep action.
        """

        self.add_step("step1")
        self.add_step("step2")
        self.add_step("step3")

    @game_step(requires=None)
    def step1(self, **kwargs):
        """
        Test step 1.
        """

        self.add_transition(("step1",))

    @game_step(requires='num')
    def step2(self, num, **kwargs):
        """
        Test step 2. Requires input.
        """

        self.add_transition(("step2", num))

    @game_step(requires=None)
    def step3(self, num, **kwargs):
        """
        Tests step 3. Requires input from previous
        step.
        """

        self.add_transition(("step3", num))

    def get_magic(self):
        """
        This is just because isinstance of is acting poorly.
        """

        return self.magic
