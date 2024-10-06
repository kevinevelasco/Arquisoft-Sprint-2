from django.db import models

class TareaBatch(models.Model):
    descripcion = models.TextField()
    estado = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.descripcion
