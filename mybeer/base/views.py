from django.shortcuts import render, render_to_response
from django.template import RequestContext, Context
from django.conf import settings


def render_home(request):
	return render_to_response('home.html', {'settings': settings, }, context_instance=RequestContext(request))
