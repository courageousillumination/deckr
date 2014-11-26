"""
This module provides all of the forms used by the deckr app.
"""

from django import forms

from deckr.models import GameDefinition, Player


class CreateGameRoomForm(forms.Form):

    """
    A simple form that can be used to create a game room.
    """

    game_id = forms.ModelChoiceField(
        queryset=GameDefinition.objects.all(),
        label='Game')


class PlayerForm(forms.ModelForm):

    """
    A simple form that will allow a user to choose their nickname.
    """

    nickname = forms.CharField(label='')

    class Meta:  # pylint: disable=C1001,W0232,C0111
        model = Player
        fields = ['nickname']


class UploadGameDefinitionForm(forms.Form):

    """
    This form will allow a user to upload a ZIP file that contains
    a game.
    """

    game_name = forms.CharField()
    file = forms.FileField()
