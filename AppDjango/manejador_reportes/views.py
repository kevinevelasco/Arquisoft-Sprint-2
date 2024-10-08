from django.http import HttpResponse
from django.shortcuts import render
from .services import obtener_cuentas_por_cobrar
from django.core.cache import cache

def generar_reporte(request, nombre_institucion, mes):
    # Crear una clave única para la caché basada en los parámetros del request
    key = f"cuentas_por_cobrar:{nombre_institucion}:{mes}"

    # Intentar recuperar los datos desde Redis
    print(key)
    cuentas_por_cobrar = cache.get(key)
    print(cuentas_por_cobrar)

    # Si no se encontraron en Redis, ejecutar la función para obtenerlas
    if cuentas_por_cobrar is None:
        print("Datos no encontrados en Redis, ejecutando la función...")
        cuentas_por_cobrar = obtener_cuentas_por_cobrar(nombre_institucion, mes)

        # Guardar los resultados en Redis por 24 horas
        cache.set(key, cuentas_por_cobrar, timeout=60*60*24)
    else:
        print("Hit Redis")

    # Pasar los resultados a la plantilla
    return render(request, 'listar.html', {'cuentas_por_cobrar': cuentas_por_cobrar})

def home(request):
    return HttpResponse("Bienvenido a la aplicación")
