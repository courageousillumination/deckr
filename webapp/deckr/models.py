"""
Contains definitions of all models for deckr.
"""

from django.db import models
from django.db.models.signals import pre_save
from os.path import join as pjoin
from django.dispatch import receiver
from django.conf import settings


class GameDefinition(models.Model):

    """
    Stores a mapping between a game definition on the
    server and a display name for the webclient.
    """

    name = models.CharField(max_length=256)
    path = models.FilePathField(path=pjoin(settings.BASE_DIR,
                                           "game_defs"),
                                allow_folders=True)

    def __unicode__(self):
        """
        Unicode representation of a Game Definition.
        """

        return "{0} located at {1}".format(self.name,
                                           self.path)


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
        return "Game room for game " + str(self.room_id)

    def maximum_occupancy(self):
        """
        Compare room occupancy with maximum limit
        """
        return self.max_players == self.player_set.all().count()

    def existing_nickname(self, nickname):
        """
        Check for duplicate nickname in room
        """
        return nickname in [x.nickname for x in self.player_set.all()]


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


@receiver(pre_save, sender=Player)
def validate_save(instance, **kwargs):
    """
    Validate player object and ability to join game room
    """
    if instance.game_room.maximum_occupancy():
        raise ValueError("Cannot join full room")
    elif instance.game_room.existing_nickname(instance.nickname):
        raise ValueError("Nickname is already in use")
    elif not 0 < len(instance.nickname) <= 128:
        raise ValueError("Nickname must be between 1 and 128 characters")
