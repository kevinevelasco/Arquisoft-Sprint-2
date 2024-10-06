from django.db import models

class Log(models.Model):
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log: {self.mensaje[:50]}"
