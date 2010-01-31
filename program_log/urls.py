from django.conf.urls.defaults import *

urlpatterns = patterns('program_log.views',
  # Search Interface
  url(r'^showschedule$', 'showdaily', name="log-show-daily"),
  url(r'^add/(?P<slot>\d+)$', 'addentry', name="log-add-entry"),
  url(r'^report/(\d{4})/(\w+)/(\w+)$', 'gen_report', name="log-gen-report"),
  url(r'^report$', 'show_reports', name="log-show-report"),
)
