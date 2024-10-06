from django.http import HttpResponse
from django.shortcuts import render
from .services import obtener_cuentas_por_cobrar  # Asegúrate de que la ruta sea correcta

def generar_reporte(request, nombre_institucion, mes):
    # Llamar a la función que obtiene las cuentas por cobrar
    print("nombre_institucion", nombre_institucion)
    print("mes", mes)
    cuentas_por_cobrar = obtener_cuentas_por_cobrar(nombre_institucion, mes)
    print(cuentas_por_cobrar)

    # Pasar los resultados a la plantilla
    return render(request, 'listar.html', {'cuentas_por_cobrar': cuentas_por_cobrar})

def home(request):
    return HttpResponse("Bienvenido a la aplicación")

