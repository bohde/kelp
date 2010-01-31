from django.conf.urls.defaults import *

urlpatterns = patterns('program_log.views',
  # Search Interface
  (r'^showschedule$', 'showdaily'),
  (r'^add/(?P<slot>\d+)$', 'addentry'),
  (r'^report/(\d{4})/(\w+)/(\w+)$', 'gen_report'),
  (r'^report$', 'show_reports'),
)
