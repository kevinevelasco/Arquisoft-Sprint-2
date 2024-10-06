import factory
from django.contrib.auth.models import User
from django.db import transaction

from manejador_cronogramas.models import Estudiante, DetalleCobroCurso, Institucion, Curso
from .models import ReciboPago, ReciboCobro, PagoProforma, FacturaElectronica
from django.utils import timezone
import random
from datetime import date

# Enumeración de meses
MESES = [
    ("Enero", 1),
    ("Febrero", 2),
    ("Marzo", 3),
    ("Abril", 4),
    ("Mayo", 5),
    ("Junio", 6),
    ("Julio", 7),
    ("Agosto", 8),
    ("Septiembre", 9),
    ("Octubre", 10),
    ("Noviembre", 11),
    ("Diciembre", 12),
]


def generar_recibos_cobro_hasta_octubre():
    """
    Genera recibos de cobro para todos los estudiantes de las instituciones
    hasta el mes actual (octubre).
    """
    # Obtener la fecha actual
    fecha_actual = timezone.now().date()
    mes_actual = fecha_actual.month  # Obtener el mes actual

    # Iniciar una transacción
    with transaction.atomic():
        # Obtener todos los estudiantes de todas las instituciones
        estudiantes = Estudiante.objects.all()

        # Recorrer cada estudiante
        for estudiante in estudiantes:
            # Recorrer cada mes en la enumeración
            for mes_nombre, mes_num in MESES:
                # Solo generar recibos hasta el mes actual
                if mes_num > mes_actual:
                    break  # Salir del bucle si el mes es posterior al actual

                # Obtener los detalles de cobro para el mes actual
                detalles_cobro = DetalleCobroCurso.objects.filter(
                        cronograma_curso__curso=estudiante.cursoEstudiante,
                        mes=mes_nombre
                )

                # Solo continuar si hay detalles de cobro para ese mes
                if detalles_cobro.exists():
                    # Calcular el monto total de los detalles de cobro
                    total_monto = sum(detalle.valor for detalle in detalles_cobro)

                    if total_monto <= 0:  # Verificar que el monto total sea mayor que 0
                        print(f"No se generará recibo para el estudiante {estudiante.nombre} para el mes {mes_nombre} debido a un monto total inválido.")
                        continue

                    # Crear un nuevo recibo de cobro
                    recibo = ReciboCobro.objects.create(
                        fecha=fecha_actual,
                        estudiante=estudiante,
                        nmonto=total_monto,  # Asegúrate de establecer nmonto aquí
                        detalle=(
                            f"Recibo de cobro para el mes de {mes_nombre}, que le corresponde a {estudiante.nombreEstudiante}, "
                            f"del grado {estudiante.cursoEstudiante.grado}, número {estudiante.cursoEstudiante.numero}, "
                            f"de la institución {estudiante.cursoEstudiante.institucion.nombreInstitucion}."
                        )
                    )

                    # Agregar cada detalle de cobro al recibo
                    for detalle in detalles_cobro:
                        recibo.detalles_cobro.add(detalle)

                    print(f"Recibo {recibo.id} generado para el estudiante {estudiante.nombreEstudiante} para el mes {mes_nombre}.")


def generar_recibos_pago():
    """
    Genera recibos de pago para todos los estudiantes de todas las instituciones.
    """
    fecha_actual = date.today()

    # Obtener todos los cursos de todas las instituciones
    cursos = Curso.objects.all()

    for curso in cursos:
        # Obtener todos los estudiantes del curso
        estudiantes = Estudiante.objects.filter(cursoEstudiante=curso)
        total_estudiantes = estudiantes.count()

        # Determinar el 70% que están al día y el 30% que no lo están
        if total_estudiantes == 0:
            continue  # Si no hay estudiantes, continuar con la siguiente institución

        num_al_dia = int(total_estudiantes * 0.7)
        estudiantes_al_dia = random.sample(list(estudiantes), num_al_dia)
        estudiantes_no_al_dia = [estudiante for estudiante in estudiantes if estudiante not in estudiantes_al_dia]

        with transaction.atomic():
            # Procesar estudiantes al día
            for estudiante in estudiantes_al_dia:
                recibos_cobro = ReciboCobro.objects.filter(estudiante=estudiante)  # Obtener todos los recibos de cobro

                for recibo_cobro in recibos_cobro:
                    # Crear el recibo de pago
                    ReciboPago.objects.create(
                        recibo_cobro=recibo_cobro,
                        fecha=fecha_actual,
                        nmonto=recibo_cobro.nmonto,
                        detalle=f"Pago total por el estudiante {estudiante.nombreEstudiante}."
                    )
                    print(f"Recibo de pago total generado para {estudiante.nombreEstudiante}: {recibo_cobro.nmonto}")

            # Procesar estudiantes no al día
            for estudiante in estudiantes_no_al_dia:
                # Obtener todos los recibos de cobro del estudiante
                recibos_cobro = list(ReciboCobro.objects.filter(estudiante=estudiante).order_by('fecha'))

                # Determinar el número aleatorio de meses a pagar (1 a 6)
                meses_a_pagar = random.randint(1, 6)

                # Calcular el índice para seleccionar los recibos de cobro a pagar
                inicio = 0
                fin = meses_a_pagar

                # Asegurarse de que no exceda el número de recibos de cobro disponibles
                if fin > len(recibos_cobro):
                    fin = len(recibos_cobro)

                # Pagar recibos de cobro desde enero hasta el número aleatorio de meses
                for recibo_cobro in recibos_cobro[inicio:fin]:
                    # Crear el recibo de pago
                    ReciboPago.objects.create(
                        recibo_cobro=recibo_cobro,
                        fecha=fecha_actual,
                        nmonto=recibo_cobro.nmonto,
                        detalle=f"Pago de recibo cobro para {estudiante.nombreEstudiante} desde enero hasta {fin}."
                    )
                    print(f"Recibo de pago generado para {estudiante.nombreEstudiante}: {recibo_cobro.nmonto}")


