"""
Register all models with the administrator interface.
"""

from django.contrib import admin

from deckr.models import GameRoom, Player

admin.site.register(GameRoom)
admin.site.register(Player)
