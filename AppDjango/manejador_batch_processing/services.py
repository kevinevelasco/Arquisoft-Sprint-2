from .models import Factura

def procesar_facturas_pendientes():
    facturas = Factura.objects.filter(pagado=False)
    for factura in facturas:
        # Lógica para procesar cada factura
        print(f"Procesando factura {factura.id}")