from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context, loader, RequestContext
from django import forms
from kelp.models import *
from django.forms import ModelForm
from django.core.paginator import Paginator
from datetime import datetime

def index(request):
	returndata = {'test':'test',}
	t = loader.get_template('base.html')
  	c = RequestContext(request,returndata)
	return HttpResponse(t.render(c))
	
	
class logblock:
	hour = None
	programming = []

	
def showdaily(request):

	blocks = ProgramBlock.objects.all().order_by('start')
	
	returndata = {'blocks':blocks,}
	t = loader.get_template('daily.html')
  	c = RequestContext(request,returndata)
	return HttpResponse(t.render(c))