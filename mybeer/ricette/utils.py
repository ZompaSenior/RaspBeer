from .models import Ricetta, CoppiaCottura


def db_get_coppie_ricetta(request, id_ricetta):
	ricetta_db = Ricetta.objects.get(pk=id_ricetta)
	return ricetta_db.coppia_cottura.all()