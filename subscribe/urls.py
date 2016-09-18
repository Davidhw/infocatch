from django.conf.urls import patterns, include, url
from subscribe import views

urlpatterns = patterns('', 
    url(r'^$',views.load_external_page_site_not_specified_in_URL),
    url(r'save',views.save),
    url(r'^(?P<url>.+)', views.load_external_page),
)
