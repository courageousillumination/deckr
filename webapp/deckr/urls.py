"""
Configure all of the URL patterns for deckr.
"""

from django.conf.urls import patterns, url, include

import socketio.sdjango

INDEX = url(r'^$',
            'deckr.views.index',
            name='deckr.index')

CREATE_GAME_ROOM = url(r'^new_game_room/',
                       'deckr.views.create_game_room',
                       name='deckr.create_game_room')

GAME_ROOM = url(r'^game_room/(?P<game_room_id>[0-9]+)/',
                'deckr.views.game_room',
                name='deckr.game_room')

TEST_SOLITAIRE = url(r'test_solitaire/', 'deckr.views.test_solitaire',
                     name='deckr.test_solitaire')

UPLOAD_NEW_GAME = url(r'^upload_new_game/',
                      'deckr.views.upload_new_game',
                      name='deckr.upload_new_game')

TEST_GAME = url(r'test_game/', 'deckr.views.test_game',
                name='deckr.test_game')

SOCKETS = url(r'^socket\.io', include(socketio.sdjango.urls))

urlpatterns = patterns(  # pylint: disable=C0103
    '',
    SOCKETS,
    INDEX,
    TEST_GAME,
    TEST_SOLITAIRE,
    CREATE_GAME_ROOM,
    UPLOAD_NEW_GAME,
    GAME_ROOM)
