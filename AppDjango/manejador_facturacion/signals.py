# signals.py en manejador_facturacion
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FacturaElectronica
from manejador_logs.services import registrar_evento

@receiver(post_save, sender=FacturaElectronica)
def log_factura_creada(sender, instance, created, **kwargs):
    if created:
        registrar_evento(f"Se ha creado una nueva factura: {instance.id}")
