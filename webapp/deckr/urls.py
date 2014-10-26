from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'deckr.views.index', name='deckr.index'),
)