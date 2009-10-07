from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

from django.contrib import databrowse

urlpatterns = patterns('kelp.views',
  # Search Interface
  (r'^$', 'index'),
  (r'^showschedule$', 'showdaily'),
  )

urlpatterns += patterns('',
  # Media
  (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media'}),
	
  # Uncomment this for admin. This should be disabled for the production site
  (r'^admin/(.*)', admin.site.root),
  (r'^databrowse/(.*)', databrowse.site.root),
  (r'^accounts/login/$', 'django.contrib.auth.views.login'),
)
