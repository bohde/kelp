"""
Urls for kelp.
"""
from django.conf.urls.defaults import *
from django.contrib import admin, databrowse
from django.views.generic.simple import direct_to_template

from models import DiskJockey, Semester, ShowBlock, Show
from program_log.models import Program, ProgramSlot, Entry, Quarter, Report, ProgramBlock
from views import kelp_logout


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'generic.html'},
        name="kelp-index"),
    url(r'^', include('kelp.program_log.urls')),
)

urlpatterns += patterns('',
  # Media
  url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media'}),

  # Uncomment this for admin. This should be disabled for the production site
  url(r'^admin/(.*)', admin.site.root),
  url(r'^databrowse/(.*)', databrowse.site.root),
  url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='kelp-login'),
  url(r'^accounts/logout/$', kelp_logout),

)
admin.site.register(DiskJockey)
admin.site.register(Semester)
admin.site.register(ShowBlock)
admin.site.register(Show)


class SlotInline(admin.TabularInline):
    "Inline Slots for Program Slots in Admin."
    model = ProgramSlot
    extra = 5

class ProgramBlockAdmin(admin.ModelAdmin):
    "Give Program Blocks the ability to program slots inline."
    inlines = (SlotInline,)

admin.site.register(Program)
admin.site.register(ProgramBlock, ProgramBlockAdmin)
admin.site.register(ProgramSlot)
admin.site.register(Entry)
admin.site.register(Quarter)
admin.site.register(Report)
