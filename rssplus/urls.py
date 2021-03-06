from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()
urlpatterns = patterns('',
    # social login stuff
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),

    url(r'^$', 'rssplus.views.home', name='home'),
    url(r'^wakemydyno.txt$', 'rssplus.views.home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^subscribe/',include('subscribe.urls')),
    url(r'^settings/',include('userSettings.urls')),
    url(r'^rss/',include('getFeeds.urls')),
)
