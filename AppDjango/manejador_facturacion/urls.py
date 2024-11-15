from django.urls import path
from .views import listar_facturas, listado_pagos_estudiante, pagar

app_name = 'manejador_facturacion'  # Esto es necesario para el namespace
urlpatterns = [
    path('', listar_facturas, name='listar_facturas'),
    path('conceptos_pago/<int:estudiante_id>/', listado_pagos_estudiante, name='listado_conceptos_pago'),
    path('pagar/', pagar, name='pagar'),
]
