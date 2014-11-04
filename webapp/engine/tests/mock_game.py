from engine.game import Game


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

    @action
    def win(self, player_id):
        self.winners.append(player_id)
        self.over = True

    @action
    def lose(self, player_id):
        self.over = True

    @action(self.restrictions)
    def restricted_action(self, player_id):
        self.winners.append(player_id)
        self.over = True

    # Restricttions
    def restrictions(self, player_id):
        self.phase != "restricted"


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
    
