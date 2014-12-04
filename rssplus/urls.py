from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rssplus.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^subscribe/',include('subscribe.urls')),
#    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root',settings.STATICFILES_DIRS, "url"})
#    url(r'^subscribe/(?P<url>\.+)', subscribe.views.load_external_page()),
)
