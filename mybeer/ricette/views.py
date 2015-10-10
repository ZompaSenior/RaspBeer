import json

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import get_template
from django.conf import settings
from django import forms
from django.core.validators import MaxLengthValidator
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict

from .models import *


#Form:  http://www.effectivedjango.com/forms.html

def valida_intero(value):
	try:
		value = int(value)
	except ValueError:
		raise ValidationError(u"%s non e' un intero." % value)


class Form_Coppia_Cottura(forms.Form):
	# validatori: https://docs.djangoproject.com/en/1.6/ref/validators/
	tempo = forms.CharField(widget=forms.TextInput(attrs={'id':'tempo', 'class':'form-control', 'length':10, 'max_length':10}), required=False, validators=[MaxLengthValidator(10), valida_intero], label="Tempo (minuti)")	
	temperatura = forms.CharField(widget=forms.TextInput(attrs={'id':'temperatura', 'class':'form-control', 'length':3, 'max_length':3}), required=False, validators=[MaxLengthValidator(3), valida_intero], label="Temperatura gradi C")	


class Form_Ricetta(forms.Form):	
	titolo = forms.CharField(widget=forms.TextInput(attrs={'id':'titolo', 'class':'form-control', 'aria-describedby':'basic-addon1'}), required=True)
	descrizione = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), required=False)  # instead of forms.Textarea
	
	#status = forms.CharField(widget=forms.HiddenInput(attrs={'name':'status', 'id':'status', 'value':'new'}), required=False)


# url(r'^ricetta/nuova/$', name='render_nuova_ricetta'),
def render_nuova_ricetta(request):
	if request.method == 'GET':
		form_ricetta = Form_Ricetta()
		form_coppia = Form_Coppia_Cottura()
		
		ricetta = []
		ricetta_id = request.GET.get('ricetta_id', 0)
		if ricetta_id not in (0,'0'):
			ricetta = db_get_ricetta(request, ricetta_id)
			form_ricetta = Form_Ricetta(initial=model_to_dict(ricetta))
		
		return render_to_response('ricetta_nuova.html', {'settings': settings, 'form_ricetta':form_ricetta, 'form_coppia':form_coppia, 'ricetta_db':ricetta}, context_instance=RequestContext(request))
		
	resp = {'html':'', 'status':0, 'ricetta_id':0}	
	if request.method == 'POST':
		post = request.POST
		
		form_ricetta = Form_Ricetta(post)
		#form_coppia = Form_Coppia_Cottura(post)
		
		cc = None
		if form_ricetta.is_valid():# and form_coppia.is_valid():
			resp['status'] = 1
# 			if form_coppia.cleaned_data['tempo'] and form_coppia.cleaned_data['temperatura']:
# 				cc = db_set_coppia_cottura(request, form_coppia)
			
			ricetta_id = post.get('ricetta_id', 0)
			if ricetta_id not in ('0', 0):
				ricetta = db_get_ricetta(request, ricetta_id)
				db_upd_ricetta(request, ricetta, form_ricetta)
			else:
				ricetta = db_set_ricetta(request, form_ricetta, cc)
			#restituisco l'id della ricetta
			resp['ricetta_id'] = ricetta.id
			
		else:
			html_template = get_template('ricetta_nuova.html')
			d = RequestContext(request, {'settings': settings, 'form_ricetta':form_ricetta, 'form_coppia':form_coppia})
			html_content = html_template.render(d)
			resp['html'] = html_content
		
	return HttpResponse(json.dumps(resp), content_type="application/json")
	

#url(r'^ricetta/lista/$', name='render_lista_ricette'),	
def render_lista_ricette(request):
	items = Ricetta.objects.all()
	
	return render_to_response('ricetta_lista.html', {'settings': settings, 'items':items}, context_instance=RequestContext(request))
	

#url(r'^ricetta/coppia/nuova/$', name='render_form_coppia_cottura'),
def render_form_coppia_cottura(request):
	resp = {'html':'', 'status':0}
	ricetta = []
	if request.method == 'GET':
		form_coppia = Form_Coppia_Cottura()
	
	if request.method == 'POST':
		post = request.POST
		ricetta_id = post.get('ricetta_id', 0)
		
		if ricetta_id:
			form_coppia = Form_Coppia_Cottura(post)
			if form_coppia.is_valid():
				ricetta = db_get_ricetta(request, ricetta_id)
				cc = db_set_coppia_cottura(request, form_coppia)
				ricetta.coppia_cottura.add(cc)
				ricetta.save()
				resp['status'] = 1
				#reset del form
				form_coppia = Form_Coppia_Cottura()
	
	html_template = get_template('ricetta_lista_coppia.html')
	d = RequestContext(request, {'ricetta_db':ricetta})
	html_content = html_template.render(d)
	resp['html_lista_cc'] = html_content
	
	html_template = get_template('ricetta_nuova_coppia.html')
	d = RequestContext(request, {'settings': settings, 'form_coppia':form_coppia, 'ricetta_db':ricetta})
	html_content = html_template.render(d)
	resp['html'] = html_content
	
	return HttpResponse(json.dumps(resp), content_type="application/json")
	

def db_set_coppia_cottura(request, form):
	cc = CoppiaCottura()
	cc.tempo = form.cleaned_data['tempo']
	cc.temperatura = form.cleaned_data['temperatura']
	cc.save()
	return cc


def db_get_ricetta(request, ricetta_id):
	ricetta = Ricetta.objects.get(pk=ricetta_id)	
	return ricetta


def db_upd_ricetta(request, ricetta, form):
	ricetta.titolo = form.cleaned_data['titolo']
	ricetta.descrizione = form.cleaned_data['descrizione']
	ricetta.save()
	return ricetta

def db_set_ricetta(request, form, cc=None):
	ricetta = Ricetta()
	ricetta.user_id = 1
	ricetta.titolo = form.cleaned_data['titolo']
	ricetta.descrizione = form.cleaned_data['descrizione']
	ricetta.save()
	
	if cc:
		ricetta.coppia_cottura.add(cc)
	ricetta.save()
	
	return ricetta
	