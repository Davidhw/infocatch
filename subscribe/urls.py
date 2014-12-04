from django.conf.urls import patterns, include, url
from subscribe import views

urlpatterns = patterns('',
    url(r'save',views.save),
    url(r'^(?P<url>.+)', views.load_external_page),
#    url(r'clickBehavior.js',
)
