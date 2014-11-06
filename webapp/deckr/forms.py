"""
This module provides all of the forms used by the deckr app.
"""

from django import forms

from deckr.models import GameDefinition


class CreateGameRoomForm(forms.Form):

    """
    A simple form that can be used to create a game room.
    """

    game_id = forms.ModelChoiceField(queryset=GameDefinition.objects.all())
