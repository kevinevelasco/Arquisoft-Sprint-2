from django.db import models

class Institucion(models.Model):
    nombreInstitucion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombreInstitucion

class Curso(models.Model):
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    grado = models.CharField(max_length=50)
    numero = models.IntegerField()
    anio = models.IntegerField()

    def __str__(self):
        return f"{self.grado} - {self.numero}"

class Estudiante(models.Model):
    nombreEstudiante = models.CharField(max_length=100)
    codigoEstudiante = models.CharField(max_length=50)
    cursoEstudiante = models.ForeignKey(Curso, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombreEstudiante

class CronogramaEstudiante(models.Model):
    estudiante = models.OneToOneField(Estudiante, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class CronogramaBase(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class DetalleCobroEstudiante(models.Model):
    cronograma_estudiante = models.ForeignKey(CronogramaEstudiante, on_delete=models.CASCADE, related_name="detalles_cobro")
    mes = models.CharField(max_length=20)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    fechaCausacion = models.DateField()
    fechaLimite = models.DateField()
    frecuencia = models.CharField(max_length=50)

    def __str__(self):
        return f"Cobro de {self.mes} - Estudiante {self.cronograma_estudiante.estudiante.nombre} - {self.valor}"


class DetalleCobroCurso(models.Model):
    cronograma_curso = models.ForeignKey(CronogramaBase, on_delete=models.CASCADE, related_name="detalles_cobro")
    mes = models.CharField(max_length=20)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    fechaCausacion = models.DateField()
    fechaLimite = models.DateField()

    def __str__(self):
        return f"Cobro de {self.mes} - Curso {self.cronograma_curso.curso.nombre} - {self.valor}"


class Descuento(models.Model):
    tipoDescuento = models.CharField(max_length=50)

    def __str__(self):
        return self.tipoDescuento
