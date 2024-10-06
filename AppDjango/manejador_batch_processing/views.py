from django.shortcuts import render

from .models import TareaBatch

def listar_tareas(request):
    tareas = TareaBatch.objects.all()
    return render(request, 'manejador_batch_processing/listar.html', {'tareas': tareas})
