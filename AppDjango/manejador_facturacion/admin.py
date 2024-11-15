from django.contrib import admin
from .models import PagoProforma, ReciboCobro, ReciboPago, FacturaElectronica

admin.site.register(PagoProforma)
admin.site.register(ReciboCobro)
admin.site.register(ReciboPago)
admin.site.register(FacturaElectronica)
