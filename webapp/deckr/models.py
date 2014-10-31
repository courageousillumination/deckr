"""
Contains definitions of all models for deckr.
"""

from django.db import models


class GameRoom(models.Model):
    """
    Contains attributes and methods for GameRoom class
    """
    room_id = models.IntegerField()
    max_players = models.IntegerField(default=8)

    def __unicode__(self):
        """
        Unicode representation of GameRoom object
        """
        return "Game Room for Game " + str(self.room_id)


class Player(models.Model):
    """
    Contains attributes and methods for Player class
    """
    player_id = models.IntegerField()
    game_room = models.ForeignKey(GameRoom)
    nickname = models.CharField(max_length=128)

    def __unicode__(self):
        """
        Unicode representation of Player class
        """
        return self.nickname
