import factory
from django.contrib.auth.models import User
from .models import Institucion, Curso, Estudiante, CronogramaEstudiante, CronogramaBase, Descuento, DetalleCobroCurso
import random
from factory.faker import Faker
from datetime import date, timedelta
from calendar import monthrange

from faker_education import SchoolProvider


class InstitucionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Institucion

    factory.Faker.add_provider(SchoolProvider)
    nombreInstitucion = factory.Faker('school_name')

class CursoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Curso

    grado = factory.Iterator(['Primero', 'Segundo', 'Tercero', 'Cuarto', 'Quinto', 'Sexto', 'Séptimo', 'Octavo', 'Noveno', 'Décimo', 'Undécimo'])
    numero = factory.Iterator([1, 2])  # Solo números 1 y 2
    anio = 2024  # Año fijo 2024
    institucion = factory.SubFactory(InstitucionFactory)


def crear_cursos_para_institucion(institucion):
    grados = ['Primero', 'Segundo', 'Tercero', 'Cuarto', 'Quinto', 'Sexto', 'Séptimo', 'Octavo', 'Noveno', 'Décimo',
              'Undécimo']
    numeros = [1, 2]
    anio = 2024

    for grado in grados:
        for numero in numeros:
            CursoFactory(grado=grado, numero=numero, anio=anio, institucion=institucion)

class EstudianteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Estudiante

    nombreEstudiante = factory.Faker('name')
    codigoEstudiante = factory.Faker('ean13')
    cursoEstudiante = factory.SubFactory(CursoFactory)


def asignar_estudiantes_a_cursos():
    # Obtener todos los cursos generados
    cursos = Curso.objects.all()

    for curso in cursos:
        # Generar entre 28 y 40 estudiantes para cada curso
        numero_estudiantes = random.randint(28, 40)
        for _ in range(numero_estudiantes):
            EstudianteFactory(cursoEstudiante=curso)


class CronogramaBaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CronogramaBase

    curso = factory.SubFactory(CursoFactory)
    codigo = factory.Faker('ean13')
    nombre = factory.Faker('sentence')


import random


def crear_cronogramas_para_curso(curso):
    # Crear cronograma para matrícula
    CronogramaBaseFactory(curso=curso, codigo=f"M-{curso.id}", nombre="Matrícula anual")

    # Crear cronograma para pensión mensual
    CronogramaBaseFactory(curso=curso, codigo=f"P-{curso.id}", nombre="Pensión mensual")

    # Crear cronograma para inglés (opcional)
    if random.choice([True, False]):  # Aproximadamente 50% de probabilidades de tener inglés
        CronogramaBaseFactory(curso=curso, codigo=f"I-{curso.id}", nombre="Curso de inglés")

def crear_cronogramas_bases():
    cursos = Curso.objects.all()  # Obtener todos los cursos
    for curso in cursos:
        crear_cronogramas_para_curso(curso)

class DetalleCobroCursoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DetalleCobroCurso

    cronograma_curso = factory.SubFactory(CronogramaBaseFactory)
    mes = factory.Iterator(['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre',
                            'Octubre', 'Noviembre', 'Diciembre'])
    fechaCausacion = factory.Faker('date_this_year')
    fechaLimite = factory.Faker('date_this_year')

    @factory.lazy_attribute
    def valor(self):
        curso = self.cronograma_curso.get_factory()
        institucion = curso.institucion

        grados = ['Primero', 'Segundo', 'Tercero', 'Cuarto', 'Quinto', 'Sexto', 'Séptimo', 'Octavo', 'Noveno', 'Décimo', 'Undécimo']
        factor_grado = (grados.index(curso.grado) + 1) / len(grados)

        random.seed(institucion.id)
        pension_base = random.randint(100000, 250000) * factor_grado
        multiplicador_matricula = random.uniform(4, 6)

        # Cobrar matrícula en Enero, pensión en los demás meses
        if self.mes == 'Enero':
            return pension_base * multiplicador_matricula
        else:
            return pension_base

    frecuencia = factory.LazyAttribute(lambda o: 'Anual' if o.mes == 'Enero' else 'Mensual')


# Función para generar cobros sin generar cronogramas
def generar_detalles_cobro_para_instituciones():
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
             'Noviembre', 'Diciembre']

    for institucion in Institucion.objects.all():
        for curso in Curso.objects.filter(institucion=institucion):
            # Obtener todos los cronogramas del curso
            cronogramas = CronogramaBase.objects.filter(curso=curso)

            for cronograma in cronogramas:
                # Factor de ajuste según el grado del curso
                grados = ['Primero', 'Segundo', 'Tercero', 'Cuarto', 'Quinto', 'Sexto', 'Séptimo', 'Octavo', 'Noveno',
                          'Décimo', 'Undécimo']
                factor_grado = (grados.index(curso.grado) + 1) / len(grados)

                random.seed(institucion.id)
                pension_base = random.randint(100000, 250000) * factor_grado
                multiplicador_matricula = random.uniform(4, 6)

                # Crear el cobro de matrícula solo una vez
                if cronograma.nombre == "Matrícula anual":  # Matrícula
                    valor = pension_base * multiplicador_matricula
                    fecha_causacion = date(curso.anio, 1, 1)
                    fecha_limite = fecha_causacion + timedelta(weeks=3)

                    DetalleCobroCurso.objects.create(
                        cronograma_curso=cronograma,
                        mes='Enero',
                        valor=valor,
                        fechaCausacion=fecha_causacion,
                        fechaLimite=fecha_limite
                    )

                # Crear los cobros de pensión y otros
                for i, mes in enumerate(meses):
                    if cronograma.nombre == "Pensión mensual":  # Pensión
                        if mes != 'Enero':
                            valor = pension_base
                            mes_actual = i + 1
                            fecha_causacion = date(curso.anio, mes_actual - 1, 1)
                            fecha_limite = date(curso.anio, mes_actual, 5)

                            DetalleCobroCurso.objects.create(
                                cronograma_curso=cronograma,
                                mes=mes,
                                valor=valor,
                                fechaCausacion=fecha_causacion,
                                fechaLimite=fecha_limite
                            )

                    elif cronograma.nombre == "Curso de inglés":  # Curso de inglés
                        if mes == 'Enero':  # O el mes que corresponda
                            valor = 200000  # Ejemplo de valor fijo
                            fecha_causacion = date(curso.anio, 1, 1)
                            fecha_limite = date(curso.anio, 1, 15)

                            DetalleCobroCurso.objects.create(
                                cronograma_curso=cronograma,
                                mes=mes,
                                valor=valor,
                                fechaCausacion=fecha_causacion,
                                fechaLimite=fecha_limite
                            )

        print(f"Generados cobros para la institución {institucion.nombreInstitucion}")


