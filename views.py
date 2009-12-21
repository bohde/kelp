from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context, loader, RequestContext
from django import forms
from kelp.models import *
from django.forms import ModelForm
from django.core.paginator import Paginator
from datetime import datetime, date, timedelta
from django.core.urlresolvers import reverse
from collections import defaultdict
from itertools import product


def index(request):
    returndata = {'test':'test',}
    t = loader.get_template('base.html')
    c = RequestContext(request,returndata)
    return HttpResponse(t.render(c))
	
def showdaily(request):

    blocks = ProgramBlock.objects.all().order_by('start')
	
    returndata = {'blocks':blocks,}
    t = loader.get_template('daily.html')
    c = RequestContext(request,returndata)
    return HttpResponse(t.render(c))
	
def addentry(request,slot):

    s = ProgramSlot.objects.get(pk=slot)
	
    if request.POST:
        n = request.POST['notes']
	if n == 'Description':
            n = ''
	
    e = Entry.objects.create(slot=s,notes=n)
    return HttpResponseRedirect(reverse("kelp.views.showdaily",))

def date_generator(begin, end, format):
    ret = begin
    delta = timedelta(1)
    while ret <= end:
        yield ret.strftime(format)
        ret += delta
    return 

def quarterly_report(request, year, quarter):
    pass
    
def gen_report(request):#, year, quarter):
    begin = (2009,10,1)
    end = (2009,12,31)
    
    date_format = "%d %b %Y"
    
    dates = date_generator(date(*begin), date(*end), date_format)

    names = ["60 Second Science", "Earth and Sky"]

    es = Entry.objects.filter(date__gte=datetime(*begin)).filter(date__lte=datetime(*end))
    es = es.select_related().all()
    
    entries = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for entry in es:
        entries[entry.date.strftime(date_format)][entry.slot.program.name][entry.notes].append(entry.time)

    def lookup(date, name):
        if entries.has_key(date) and entries[date].has_key(name):
            ret_notes = ((note, sorted(time.strftime('%H:%M') for time in times))
                         for note, times in entries[date][name].iteritems())
            return (date, name, ret_notes)
                                 
        return (date, name, ())

    display_entries = (lookup(a_date, name) for a_date, name in product(dates, names))

    return render_to_response("report.csv", {"entries":display_entries}, mimetype='text/csv')
