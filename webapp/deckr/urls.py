from django.conf.urls import patterns, url

INDEX = url(r'^$', 'deckr.views.index', name='deckr.index')
urlpatterns = patterns('', INDEX)
