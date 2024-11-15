from datetime import datetime
import requests
from manejador_cronogramas.models import Curso, Institucion
from .models import FacturaElectronica
from django.shortcuts import render, redirect
from .models import Estudiante, ReciboCobro, ReciboPago
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib import messages
import time
from django.contrib.auth.decorators import login_required
from AppDjango.auth0backend import getRole, getNickname


def listar_facturas(request):
    facturas = FacturaElectronica.objects.all()
    return render(request, 'manejador_facturacion/listar.html', {'facturas': facturas})


def obtener_institucion_por_estudiante_id(estudiante_id):
    try:
        estudiante = Estudiante.objects.get(id=estudiante_id)
        institucion = estudiante.cursoEstudiante.institucion
        return institucion.nombreInstitucion.replace(' ', '_')
    except Estudiante.DoesNotExist:
        return "Estudiante no encontrado"
    except Curso.DoesNotExist:
        return "Curso no encontrado"
    except Institucion.DoesNotExist:
        return "Institución no encontrada"


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
def listado_pagos_estudiante(request, estudiante_id):
    #traemos la institucion del estudiante
    nombre_institucion = obtener_institucion_por_estudiante_id(estudiante_id)
    role = getRole(request)
    nickname = getNickname(request)
    if role == 'Auxiliar contable':
        if verificar_institucion(nickname, nombre_institucion):
            try:
                # Obtener el estudiante
                estudiante = Estudiante.objects.get(id=estudiante_id)
            except Estudiante.DoesNotExist:
                raise Http404("Estudiante no encontrado")

            # Obtener todos los recibos de cobro relacionados con este estudiante
            recibos_cobro = ReciboCobro.objects.filter(estudiante=estudiante).order_by('fecha')

            # Crear un listado con los detalles de los pagos y los recibos
            listado_detalles = []
            for recibo in recibos_cobro:
                # Buscar el pago realizado para ese recibo
                pago = ReciboPago.objects.filter(recibo_cobro=recibo).first()

                # Calcular el monto total pagado y el saldo para este recibo
                monto_pagado = pago.nmonto if pago else 0
                saldo = recibo.nmonto - monto_pagado

                listado_detalles.append({
                    'recibo_cobro_id': recibo.id,
                    'detalle': recibo.detalle,
                    'monto_total': recibo.nmonto,
                    'monto_pagado': monto_pagado,
                    'saldo': saldo,
                    'recibo_pago_id': pago.id if pago else None  # ID del pago si existe
                })

            return render(request, 'listado_pagos_estudiante.html', {
                'estudiante': estudiante,
                'listado_detalles': listado_detalles,
            })
        else:
            return JsonResponse({"message": "La institución a la cual quieres acceder no es a la que perteneces"})
    else:
        return HttpResponse("Unauthorized User")

@login_required
def pagar(request):
    role = getRole(request)
    if role == 'Auxiliar contable':
        if request.method == "POST":
            # Iterar sobre todos los campos del formulario que contienen el prefix 'pagar_'
            for key, value in request.POST.items():
                if key.startswith('pagar_'):
                    # El recibo_cobro_id es el valor del botón de pago (value del botón)
                    recibo_cobro_id = value
                    # Recuperar el recibo de cobro correspondiente
                    recibo_cobro = ReciboCobro.objects.get(id=recibo_cobro_id)

                    # Crear un recibo de pago
                    recibo_pago = ReciboPago(
                        fecha=datetime.now(),
                        nmonto=recibo_cobro.nmonto,  # El monto que se paga es igual al saldo pendiente
                        detalle="Pago de recibo de cobro #" + str(recibo_cobro.id),
                        recibo_cobro_id=recibo_cobro.id
                    )

                    # Guardar el recibo de pago en la base de datos
                    recibo_pago.save()

                    # Pausar la ejecución durante 5 segundos
                    time.sleep(5)

            # Después de procesar el pago, redirigir a la vista de listado de pagos del estudiante
            return redirect(request.META.get('HTTP_REFERER'))

        # Si no es un POST, redirigir a la página de inicio
        return redirect('home')
    else:
        return HttpResponse("Unauthorized User")
