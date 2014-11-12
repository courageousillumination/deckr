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

STAGING_AREA = url(r'^game_room_staging_area/(?P<game_room_id>[0-9]+)/',
                   'deckr.views.game_room_staging_area',
                   name='deckr.game_room_staging_area')

GAME_ROOM = url(r'^game_room/(?P<game_room_id>[0-9]+)/',
                'deckr.views.game_room',
                name='deckr.game_room')

UPLOAD_NEW_GAME = url(r'^upload_new_game/',
                      'deckr.views.upload_new_game',
                      name='deckr.upload_new_game')

TEST_GAME = url(r'test_game/', 'deckr.views.test_game', name='deckr.test_game')

SOCKETS = url(r'^socket\.io', include(socketio.sdjango.urls))

urlpatterns = patterns(  # pylint: disable=C0103
    '',
    SOCKETS,
    INDEX,
    STAGING_AREA,
    CREATE_GAME_ROOM,
    UPLOAD_NEW_GAME,
    GAME_ROOM,
    TEST_GAME)
