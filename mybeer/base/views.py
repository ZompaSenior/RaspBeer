from django.shortcuts import render, render_to_response
from django.template import RequestContext, Context
from django.conf import settings

from ricette.views import db_get_ricette

def render_home(request):
	items = {}
	
	ricette = db_get_ricette(request)
	items['ricette'] = ricette

	return render_to_response('home.html', {'settings': settings, 'items':items}, context_instance=RequestContext(request))	