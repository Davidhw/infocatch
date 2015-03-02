from django.conf.urls import patterns, url
from userSettings import views

urlpatterns = patterns('',
    url(r'^$', views.changeSettings, name = "settings"),
)
