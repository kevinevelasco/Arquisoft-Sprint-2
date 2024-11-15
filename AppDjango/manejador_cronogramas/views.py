from django.shortcuts import render
from .models import CronogramaBase

def listar_cronogramas(request):
    cronogramas = CronogramaBase.objects.all()
    return render(request, 'manejador_cronogramas/listar.html', {'cronogramas': cronogramas})
