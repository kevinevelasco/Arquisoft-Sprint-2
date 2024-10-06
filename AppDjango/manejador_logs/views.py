from django.shortcuts import render
from .models import Log

def listar_logs(request):
    logs = Log.objects.all()
    return render(request, 'manejador_logs/listar.html', {'logs': logs})
