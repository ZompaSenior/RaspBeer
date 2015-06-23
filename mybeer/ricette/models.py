from django.db import models


class CoppiaCottura(models.Model):
	id = models.AutoField(primary_key=True)
	tempo = models.CharField(max_length=10)
	temperatura = models.IntegerField(max_length=3, default=30)
	created = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)
	

class Ricetta(models.Model):
	id = models.AutoField(primary_key=True)
	user_id = models.IntegerField(max_length=12)
	titolo = models.CharField(max_length=256)
	descrizione = models.TextField()
	coppia_cottura = models.ManyToManyField(CoppiaCottura, null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)