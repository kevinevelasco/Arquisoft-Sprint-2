from django.shortcuts import render
# from .models import DetalleCobroCurso

def generar_reporte(request):
    # Lógica para generar reportes sobre los cobros de cursos
    # reportes = DetalleCobroCurso.objects.all()
    return render(request, 'manejador_reportes/listar.html', {'reportes': None})

from django.http import HttpResponse

def home(request):
    return HttpResponse("Bienvenido a la aplicación")
