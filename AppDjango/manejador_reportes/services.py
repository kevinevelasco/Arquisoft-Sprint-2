from django.db.models import Q
from datetime import date, timedelta

from manejador_cronogramas.models import Curso, DetalleCobroCurso
from manejador_facturacion.models import ReciboCobro, ReciboPago


from django.db import connection

def obtener_cuentas_por_cobrar(nombre_institucion, mes):
    query = """
    SELECT 
        rc.nmonto AS monto_recibo,
        dc.mes,
        dc.valor AS valor_detalle,
        rc.estudiante_id,
        es."nombreEstudiante" AS nombre_estudiante,
        c.grado AS nombre_grado,
        i."nombreInstitucion" AS nombre_institucion,
        cb.nombre AS nombre_concepto,
        cb.codigo
    FROM 
        public.manejador_facturacion_recibocobro rc
    JOIN 
        public.manejador_facturacion_recibocobro_detalles_cobro rcdc ON rc.id = rcdc.recibocobro_id
    JOIN 
        public.manejador_cronogramas_detallecobrocurso dc ON rcdc.detallecobrocurso_id = dc.id
    LEFT JOIN 
        public.manejador_facturacion_recibopago rp ON rc.id = rp.recibo_cobro_id
    JOIN 
        public.manejador_cronogramas_estudiante es ON rc.estudiante_id = es.id
    JOIN 
        public.manejador_cronogramas_curso c ON es."cursoEstudiante_id" = c.id
    JOIN 
        public.manejador_cronogramas_institucion i ON c.institucion_id = i.id
    JOIN 
        public.manejador_cronogramas_cronogramabase cb ON dc.cronograma_curso_id = cb.id
    WHERE
        i."nombreInstitucion" = %s AND
        dc.mes = %s AND
        rp.id IS NULL;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [nombre_institucion, mes])
        rows = cursor.fetchall()

    # Convertir los valores Decimal a float antes de retornar
    processed_rows = [
        (
            float(row[0]),  # monto_recibo
            row[1],         # mes
            float(row[2]),  # valor_detalle
            row[3],         # estudiante_id
            row[4],         # nombre_estudiante
            row[5],         # nombre_grado
            row[6],         # nombre_institucion
            row[7],         # nombre_concepto
            row[8]          # codigo
        )
        for row in rows
    ]

    return processed_rows


