from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from userSettings import views

#http://stackoverflow.com/questions/20963856/improperlyconfigured-the-included-urlconf-project-urls-doesnt-have-any-patte
#http://stackoverflow.com/questions/6266415/django-class-based-generic-view-no-url-to-redirect-to
urlpatterns = patterns('',
url(r'^$', views.changeSettings.as_view(success_url=reverse_lazy('home')), name = "settings"),
)
