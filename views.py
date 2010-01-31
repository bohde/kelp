from collections import defaultdict
from datetime import date, timedelta
from django.contrib.auth import logout

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import loader, RequestContext
from kelp.models import *

from django.contrib.auth.decorators import login_required, permission_required

def index(request):
    returndata = {'test':'test',}
    t = loader.get_template('base.html')
    c = RequestContext(request,returndata)
    return HttpResponse(t.render(c))

class HttpResponseNotAuthorized(HttpResponse):
    status_code = 401

    def __init__(self, redirect_to):
        HttpResponse.__init__(self)
        self['WWW-Authenticate'] = 'Basic realm="UM System Single-Sign-On Login"'

def kelp_logout(request):
    logout(request)
    return HttpResponseNotAuthorized(reverse("kelp.views.index"))

