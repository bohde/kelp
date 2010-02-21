# Create your views here.
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from parsers import get_sci, get_psych

@login_required
def sci_am(request, program, feed):
    items = feed()
    return render_to_response("programming/sciam.html", locals(),
                              context_instance=RequestContext(request))

def sixty_second_sci(request, program):
    return sci_am(request, program, get_sci)

def sixty_second_psych(request, program):
    return sci_am(request, program, get_psych)
