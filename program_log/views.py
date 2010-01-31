from collections import defaultdict
from datetime import date, timedelta
from django.contrib.auth import logout

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import loader, RequestContext
from models import *
from django.contrib.auth.decorators import login_required, permission_required

try:
    from itertools import product
except:
    def product(*args, **kwds):
        """
        nasty hack to get around product not being in 2.5
        """
        # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
        # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
        pools = map(tuple, args) * kwds.get('repeat', 1)
        result = [[]]
        for pool in pools:
            result = [x+[y] for x in result for y in pool]
        for prod in result:
            yield tuple(prod)

@login_required	
def showdaily(request):

    blocks = ProgramBlock.objects.all().order_by('start')
	
    returndata = {'blocks':blocks,}
    t = loader.get_template('daily.html')
    c = RequestContext(request,returndata)
    return HttpResponse(t.render(c))

@login_required	
def addentry(request,slot):

    s = ProgramSlot.objects.get(pk=slot)
	
    if request.POST:
        n = request.POST['notes']
	if n == 'Description':
            n = ''
	
    e = Entry.objects.create(slot=s,notes=n)
    return HttpResponseRedirect(reverse("log-show-daily",))

@permission_required('kelp.view_reports')
def show_reports(request):
    begin = Entry.get_first_date()
    today = date.today()

    quarters = Quarter.objects.order_by('begin').all()
    
    report_slugs = [r.slug for r in Report.objects.all()]

    def compare(first, second):
        return first.month < second.month or (second.month == first.month and first.day < second.day)

    def quarter_gen(begin, end):
        if begin:
            while begin < today:
                yield (begin.year, (quarter.id for quarter in quarters 
                                     if compare(begin, quarter.end) and compare(quarter.begin, end)))
                begin = begin.replace(year=(begin.year+1))
        return 

    return render_to_response("reports.html", {"reports":quarter_gen(begin, today)
                                               , "slugs":report_slugs})
def date_generator(delta):
    def inner(begin, end, format):
        ret = begin
        while ret <= end:
            yield ret.strftime(format)
            ret += delta
        return 
    return inner

@permission_required('kelp.view_reports')
def gen_report(request, year, quarter, slug):
    try:
        q = Quarter.objects.get(pk=quarter)
        begin = q.begin.replace(year=int(year))
        end = q.end.replace(year=int(year))
        names = [p.name for p in Report.objects.get(slug=slug).program.all()]
    except:
        raise Http404

    date_format = "%d %b %Y"
    
    dates = date_generator(timedelta(1))(begin, end, date_format)

    es = Entry.objects.filter(date__gte=begin).filter(date__lte=end)
    es = es.select_related().all()
    
    
    # Group the times and notes
    entries = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for entry in es:
        entries[entry.date.strftime(date_format)][entry.slot.program.name][entry.notes].append(entry.time)


    # Make a generator to put the data in tuples instead of a dict
    def lookup(date, name):
        if entries.has_key(date) and entries[date].has_key(name):
            ret_notes = ((note, sorted(time.strftime('%H:%M') for time in times))
                         for note, times in entries[date][name].iteritems())
            return (date, name, ret_notes)
                                 
        return (date, name, ())

    display_entries = (lookup(a_date, name) for a_date, name in product(dates, names))

    return render_to_response("report.csv", {"entries":display_entries}, mimetype='text/csv')
