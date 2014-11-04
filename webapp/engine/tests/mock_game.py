from engine.game import Game, action


class MockGame(Game):

    def __init__(self):
        self.winners = []
        self.over = False
        self.is_setup = False

    def set_up(self):
        self.is_setup = True
        self.phase = "restricted"

    def is_over(self):
        return self.over

    def winners(self):
        return self.winners
    
    # Restricttions
    def restrictions(self, player_id):
        self.phase != "restricted"

    @action
    def win(self, player_id):
        self.winners.append(player_id)
        self.over = True

    @action
    def lose(self, player_id):
        self.over = True

    @action(restriction = restrictions)
    def restricted_action(self, player_id):
        self.winners.append(player_id)
        self.over = True




"""
---
game:
    name: "Test Game"
    max_players: 1
    zones:
        - name: Zone1
          stacked: True
    region:
        - name: Region 1
        - zones:
            - "Zone 1"
            - "Zone 2"
    player-attributes:
        - life: integer
"""

"""
---
card:
{% for n in range(1, 13) %}
    name: "8 of hearts"
    number: [1-8]
    
"""