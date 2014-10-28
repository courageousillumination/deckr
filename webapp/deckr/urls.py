from django.conf.urls import patterns, url, include

import socketio.sdjango

INDEX = url(r'^$', 'deckr.views.index', name='deckr.index')
SOCKETS = url("^socket\.io", include(socketio.sdjango.urls))

urlpatterns = patterns('', SOCKETS, INDEX)
