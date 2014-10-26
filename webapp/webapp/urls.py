from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webapp.views.home', name='home'),
    url(r'^', include('deckr.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
