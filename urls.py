from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

from django.contrib import databrowse

urlpatterns = patterns('kelp.views',
  # Search Interface
  (r'^$', 'index'),
  (r'^showschedule$', 'showdaily'),
  (r'^add/(?P<slot>\d+)$', 'addentry'),
  (r'^report/(\d{4})/(\w+)/(\w+)$', 'gen_report'),
  (r'^report$', 'show_reports'),
)

urlpatterns += patterns('',
  # Media
  (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media'}),
	
  # Uncomment this for admin. This should be disabled for the production site
  (r'^admin/(.*)', admin.site.root),
  (r'^databrowse/(.*)', databrowse.site.root),
  (r'^accounts/login/$', 'django.contrib.auth.views.login'),
)
