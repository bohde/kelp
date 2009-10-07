from django.contrib import admin
from kelp.models import *

class SlotInline(admin.TabularInline):
	model = ProgramSlot
	extra = 5
	
class ProgramBlockAdmin(admin.ModelAdmin):
	inlines = (SlotInline,)
	

admin.site.register(Program)
admin.site.register(ProgramBlock,ProgramBlockAdmin)
admin.site.register(ProgramSlot)
admin.site.register(Entry)
admin.site.register(DiskJockey)
admin.site.register(Semester)
admin.site.register(ShowBlock)
admin.site.register(Show)
