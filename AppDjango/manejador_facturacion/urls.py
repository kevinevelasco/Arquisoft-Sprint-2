from django.urls import path
from .views import listar_facturas

urlpatterns = [
    path('', listar_facturas, name='listar_facturas'),
]
