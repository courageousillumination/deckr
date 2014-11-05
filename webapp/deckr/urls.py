"""
Configure all of the URL patterns for deckr.
"""

from django.conf.urls import patterns, url, include

import socketio.sdjango

INDEX = url(r'^$', 'deckr.views.index', name='deckr.index')
CREATE_GAME_ROOM = url(r'^new_game_room/', 'deckr.views.create_game_room',
	name='deckr.create_game_room')
SOCKETS = url(r'^socket\.io', include(socketio.sdjango.urls))

urlpatterns = patterns('', SOCKETS, INDEX, CREATE_GAME_ROOM)