from django.db import models

from manejador_cronogramas.models import DetalleCobroCurso, Estudiante


class PagoProforma(models.Model):
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    condiciones = models.TextField()
    recibo_cobro = models.OneToOneField('ReciboCobro', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Pago {self.id} - {self.monto}"

class ReciboCobro(models.Model):
    fecha = models.DateField()
    nmonto = models.DecimalField(max_digits=10, decimal_places=2)
    detalle = models.TextField()
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, default=None, null=True)
    detalles_cobro = models.ManyToManyField(DetalleCobroCurso, related_name='recibos')

    def calcular_monto_total(self):
        return sum(detalle.valor for detalle in self.detalles_cobro.all())

    def __str__(self):
        return f"Recibo {self.id} - {self.nmonto}"

class ReciboPago(models.Model):
    recibo_cobro = models.OneToOneField(ReciboCobro, on_delete=models.CASCADE, null=True)
    fecha = models.DateField()
    nmonto = models.DecimalField(max_digits=10, decimal_places=2)
    detalle = models.TextField()

    def __str__(self):
        return f"Recibo Pago {self.id} - {self.nmonto}"

class FacturaElectronica(models.Model):
    recibo_pago = models.OneToOneField(ReciboPago, on_delete=models.CASCADE, null=True)
    CUFE = models.CharField(max_length=50)
    fecha = models.DateField()
    nmonto = models.DecimalField(max_digits=10, decimal_places=2)
    detalle = models.TextField()

    def __str__(self):
        return f"Factura {self.CUFE}"
