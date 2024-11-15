from django.http import JsonResponse
from django.shortcuts import render
from .services import obtener_cuentas_por_cobrar, obtener_cartera_general
import redis
import json
from django.contrib.auth.decorators import login_required
from AppDjango.auth0backend import getRole, getNickname
import requests


# Función para verificar el nickname e institución en la API
def verificar_institucion(nickname, nombre_institucion):
    url = f"http://10.128.0.7:8080/instituciones/institution/{nickname}/"
    try:
        response = requests.get(url)
        data = response.json()
        
        # Si devuelve error, la verificación falla
        if 'error' in data:
            return False
        
        # Verifica si la institución recibida coincide con la proporcionada
        print("Se obtienen los datos de la API:", data, "con la URL de la API:", url)
        return data.get("institution") == nombre_institucion
    except requests.RequestException as e:
        print(f"Error al verificar la institución: {e}")
        return False
    # credenciales_validas = {
    #     'aux-jose-1': 'Western_Peaks_Elementary',
    #     'aux-camila-1': 'Ravenna_High_School'
    # }
    
    # return credenciales_validas.get(nickname) == nombre_institucion

@login_required
def generar_reporte(request, nombre_institucion, mes):
    role = getRole(request)
    nickname = getNickname(request)
    if role == 'Auxiliar contable':
        if verificar_institucion(nickname, nombre_institucion):
            key = f"cuentas_por_cobrar:{nombre_institucion}:{mes}"
            print(f"Key: {key}")

            r = redis.StrictRedis(host='10.128.0.5', port=6379, db=0)
            cuentas_por_cobrar = r.get(key)

            if cuentas_por_cobrar is not None:
                cuentas_por_cobrar = json.loads(cuentas_por_cobrar.decode('utf-8'))
                print("Hit Redis")
            else:
                print("No se encontraron datos en Redis, ejecutando la función...")
                nombre_institucion_con_espacios = nombre_institucion.replace('_', ' ')
                mes_con_espacios = mes.replace('_', ' ')
                
                try:
                    cuentas_por_cobrar = obtener_cuentas_por_cobrar(nombre_institucion_con_espacios, mes_con_espacios)
                    print("Datos obtenidos de la función:", cuentas_por_cobrar)
                    r.set(key, json.dumps(cuentas_por_cobrar), ex=60 * 60 * 24)
                except Exception as e:
                    print(f"Error al obtener cuentas por cobrar: {e}")
                    cuentas_por_cobrar = []

            return render(request, 'listar.html', {'cuentas_por_cobrar': cuentas_por_cobrar})
        else:
            return JsonResponse({"message": "La institución a la cual quieres acceder no es a la que perteneces"})
    else:
        return JsonResponse({"message": "Unauthorized User"})

@login_required
def generar_cartera(request, nombre_institucion, mes):
    role = getRole(request)
    nickname = getNickname(request)
    if role == 'Auxiliar contable':
        if verificar_institucion(nickname, nombre_institucion):
            key = f"cartera_general:{nombre_institucion}:{mes}"
            print(f"Key: {key}")

            r = redis.StrictRedis(host='10.128.0.5', port=6379, db=0)
            cartera_general = r.get(key)

            if cartera_general is not None:
                cartera_general = json.loads(cartera_general.decode('utf-8'))
                print("Hit Redis")
            else:
                print("No se encontraron datos en Redis, ejecutando la función...")
                nombre_institucion_con_espacios = nombre_institucion.replace('_', ' ')
                mes_con_espacios = mes.replace('_', ' ')

                try:
                    cartera_general = obtener_cartera_general(nombre_institucion_con_espacios, mes_con_espacios)
                    print("Datos obtenidos de la función:", cartera_general)
                    r.set(key, json.dumps(cartera_general), ex=60 * 60 * 24)
                except Exception as e:
                    print(f"Error al obtener cartera general: {e}")
                    cartera_general = []
            return render(request, 'cuentas.html', {'cartera_general': cartera_general})
        else:
            return JsonResponse({"message": "La institución a la cual quieres acceder no es a la que perteneces"})
    else:
        return JsonResponse({"message": "Unauthorized User"})

def home(request):
    return JsonResponse({"message": "Bienvenido a la aplicación"})
