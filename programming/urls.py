from django.conf.urls.defaults import *
from programming.views import *


urlpatterns = patterns('',
  # Search Interface
  url(r'^sci/(?P<program>\d+)$', sixty_second_sci, name="programming-sci"),
  url(r'^psych/(?P<program>\d+)$', sixty_second_psych, name="programming-psych"),
)
