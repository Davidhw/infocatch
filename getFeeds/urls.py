from django.conf.urls import patterns, include, url
from getFeeds import views
import rssplus
from django.core.urlresolvers import reverse_lazy

urlpatterns = patterns('',
    url(r'^$',rssplus.views.home),
    url(r'^(?P<userName>\w+)/$',views.RSSFeed),
)
