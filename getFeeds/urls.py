from django.conf.urls import patterns, include, url
from getFeeds import views
from rssplus.views import home
import rssplus
from django.core.urlresolvers import reverse_lazy

urlpatterns = patterns('',
    url(r'^$',home),
    url(r'^(?P<userName>\w+)/$',views.RSSFeed),
)
