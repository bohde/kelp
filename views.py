from collections import defaultdict
from datetime import date, timedelta
from django.contrib.auth import logout

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import loader, RequestContext
from kelp.models import *

from django.contrib.auth.decorators import login_required, permission_required

class HttpResponseNotAuthorized(HttpResponseRedirect):
    status_code = 401

    def __init__(self, redirect_to):
        HttpResponseRedirect.__init__(self, redirect_to)
        self['WWW-Authenticate'] = 'Basic realm="UM System Single-Sign-On Login"'

def kelp_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("kelp.views.index"))

