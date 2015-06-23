from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #Percorsi librerie e css
   	(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.CSS_ROOT}),
	(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.JS_ROOT}),
	(r'^img/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.IMG_ROOT}),
	(r'^res/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.RES_ROOT}),

    
	url(r'^$', 'base.views.render_home', name='render_home'),
	url(r'^ricetta/nuova/$', 'ricette.views.render_nuova_ricetta', name='render_nuova_ricetta'),
	url(r'^ricetta/lista/$', 'ricette.views.render_lista_ricette', name='render_lista_ricette'),

	url(r'^admin/', include(admin.site.urls)),
)
