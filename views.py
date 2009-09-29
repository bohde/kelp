from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context, loader, RequestContext
from django import forms
from kelp.models import *
from django.forms import ModelForm
from django.core.paginator import Paginator

def index(request):
	returndata = {'test':'test',}
	t = loader.get_template('base.html')
  	c = RequestContext(request,returndata)
	return HttpResponse(t.render(c))