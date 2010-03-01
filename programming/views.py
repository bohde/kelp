# Create your views here.
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse

from parsers import load_sci, load_psych

from models import ProgrammingAudio, ProgrammingFeed

@login_required
def feed(request, program, feed):
    prog = get_object_or_404(ProgrammingFeed, pk=feed)
    prog.refresh_feed()
    ret = {"feed": prog,
           "program":program,
           "entries":prog.programmingaudio_set.all()}
    return render_to_response("programming/sciam.html", ret,
                              context_instance=RequestContext(request))

@login_required
def feeds(request):
    feeds = ProgrammingFeed.objects.all().only("title", "short_name")
    ret = {"feeds":feeds,
           "program":0,
           }
    return render_to_response("programming/feeds.html", ret, 
                              context_instance=RequestContext(request))
