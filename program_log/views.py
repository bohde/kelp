from collections import defaultdict
from datetime import date, timedelta

from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from models import *


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
    blocks = ProgramSlot.get_slots()
    return render_to_response("daily.html", {"blocks":blocks},
                              context_instance=RequestContext(request))

@login_required
def show_this_show(request):
    blocks = ProgramSlot.next_n_hours(3)
    return render_to_response("daily.html", {"blocks":blocks},
                              context_instance=RequestContext(request))

@login_required	
def addentry(request,slot):
    HOURS_LEEWAY = 1
    s = get_object_or_404(ProgramSlot, pk=slot)
    if request.method == "POST":
        n = ''
        try:
            n = request.POST['notes']
            if n == "Title":
                n = ''
        except KeyError:
            pass
        if Entry.add_entry(request.user, s, n, HOURS_LEEWAY):
            return HttpResponseRedirect(reverse("log-show-current",))
        return render_to_response("error.html",
                        {"message":"You attempted to add the entry out of the time range."},
                        context_instance=RequestContext(request))
    return HttpResponseRedirect(reverse("log-show-current",))

@permission_required('kelp.view_reports')
def show_reports(request):
    """ Generate a list of quarters from the first entry to now. """
    begin = Entry.get_first_date()
    today = date.today()

    quarters = Quarter.objects.order_by('begin').all()
    
    report_slugs = [r.slug for r in Report.objects.all()]

    def compare(first, second):
        """ Return if the first, disregarding the year is less than the second. """
        return first.month < second.month or (second.month == first.month and first.day <= second.day)

    def quarter_gen(begin, end):
        """ Return a tuple of (year, (q1,..q4)) for all quarters between the begin and end """
        if begin:
            while begin <= end:
                yield (begin.year, (quarter.id for quarter in quarters 
                                     if compare(begin, quarter.end) and compare(quarter.begin, end)))
                begin = begin.replace(year=(begin.year+1))
        return 

    return render_to_response("reports.html", {"reports":quarter_gen(begin, today)
                                               , "slugs":report_slugs}
                              ,context_instance=RequestContext(request))

def date_range(begin, end, delta=timedelta(1), format="%d %b %Y"):
    """ Yields all the dates for a given delta. Like an xrange but for dates. """
    ret = begin
    while ret <= end:
        yield ret.strftime(format)
        ret += delta
    return 

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
    
    dates = date_range(begin, end, format=date_format)

    es = Entry.objects.filter(date__gte=begin).filter(date__lte=end)
    es = es.select_related().all()
    
    # Group the times and notes
    # entries = {'01 January 2001':{'program':{'program_desc':[(date...)]}}}
    entries = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for entry in es:
        d = entry.date.strftime(date_format)
        name = entry.slot.program.name
        if entry.notes:
            entries[d][name][entry.notes].append(entry.time)

    # Make a generator to put the data in tuples instead of a dict
    def lookup(date, name):
        if entries.has_key(date) and entries[date].has_key(name):
            ret_notes = ((note, sorted(time.strftime('%H:%M') for time in times))
                         for note, times in entries[date][name].iteritems())
            return (date, name, ret_notes)
                                 
        return (date, name, ())

    display_entries = (lookup(a_date, name) for a_date, name in product(dates, names))

    return render_to_response("report.csv", {"entries":display_entries}, mimetype='text/csv')
