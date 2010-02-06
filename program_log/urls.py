from django.conf.urls.defaults import *
from program_log.views import *


urlpatterns = patterns('',
  # Search Interface
  url(r'^showschedule$', showdaily, name="log-show-daily"),
  url(r'^show$', show_this_show, name="log-show-current"),                       
  url(r'^add/(?P<slot>\d+)$', addentry, name="log-add-entry"),
  url(r'^report/(\d{4})/(\w+)/(\w+)$', gen_report, name="log-gen-report"),
  url(r'^report$', show_reports, name="log-show-report"),
)
