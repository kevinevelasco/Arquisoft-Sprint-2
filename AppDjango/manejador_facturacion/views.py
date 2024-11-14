from datetime import datetime

from manejador_cronogramas.models import DetalleCobroCurso
from .models import FacturaElectronica
from django.shortcuts import render, redirect
from .models import Estudiante, ReciboCobro, ReciboPago
from django.http import Http404, HttpResponse
from django.contrib import messages
import time


def listar_facturas(request):
    facturas = FacturaElectronica.objects.all()
    return render(request, 'manejador_facturacion/listar.html', {'facturas': facturas})


def listado_pagos_estudiante(request, estudiante_id):
    try:
        # Obtener el estudiante
        estudiante = Estudiante.objects.get(id=estudiante_id)
    except Estudiante.DoesNotExist:
        raise Http404("Estudiante no encontrado")

    # Obtener todos los recibos de cobro relacionados con este estudiante
    recibos_cobro = ReciboCobro.objects.filter(estudiante=estudiante).order_by('fecha')

    # Obtener todos los pagos realizados para estos recibos
    pagos_realizados = ReciboPago.objects.filter(recibo_cobro__estudiante=estudiante).order_by('fecha')

    # Crear un listado con los detalles de los pagos y los recibos
    listado_detalles = []
    for recibo in recibos_cobro:
        # Buscar todos los pagos realizados para ese recibo
        pagos = pagos_realizados.filter(recibo_cobro=recibo)

        # Calcular el monto total pagado para este recibo
        monto_pagado = sum(pago.nmonto for pago in pagos)

        saldo = recibo.nmonto - monto_pagado

        listado_detalles.append({
            'recibo_cobro_id': recibo.id,  # ID del recibo de cobro
            'detalle': recibo.detalle,
            'monto_total': recibo.nmonto,
            'monto_pagado': monto_pagado,
            'saldo': saldo,
            'pagos': pagos  # Lista de pagos realizados para este recibo
        })

    return render(request, 'listado_pagos_estudiante.html', {
        'estudiante': estudiante,
        'listado_detalles': listado_detalles,
    })

def pagar(request):
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
