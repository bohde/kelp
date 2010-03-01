from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
  url(r'^$', feeds, name="programming-list-feeds"),                       
  url(r'^(?P<feed>\w+)/(?P<program>\d+)$', feed, name="programming-feed"),
)

