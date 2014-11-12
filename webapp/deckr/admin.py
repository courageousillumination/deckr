"""
Register all models with the administrator interface.
"""

from django.contrib import admin

from deckr.models import GameRoom, Player, GameDefinition

admin.site.register(GameRoom)
admin.site.register(Player)
admin.site.register(GameDefinition)
