from django.shortcuts import render
from .models import FacturaElectronica

def listar_facturas(request):
    facturas = FacturaElectronica.objects.all()
    return render(request, 'manejador_facturacion/listar.html', {'facturas': facturas})
