from django.core.management import BaseCommand
from manejador_reportes.services import obtener_cuentas_por_cobrar
from manejador_cronogramas.models import Institucion
from django.core.cache import cache
import logging
import redis
import json

logger = logging.getLogger(__name__)


class Command(BaseCommand):
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

    def handle(self, *args, **kwargs):
        try:
            # Conectar a Redis
            r = redis.StrictRedis(host='10.128.0.5', port=6379, db=0)

            # Probar almacenando un valor
            test_key = 'test_key'
            test_value = 'Hello, Redis!'
            r.set(test_key, test_value)

            # Intentar recuperar el valor almacenado
            retrieved_value = r.get(test_key)

            if retrieved_value:
                print(f"Connection to Redis successful! Stored value: {retrieved_value.decode('utf-8')}")
            else:
                print("Failed to store or retrieve data from Redis.")

            # Generar reportes de cuentas por cobrar
            logger.info("Iniciando la generación de reportes...")
            for institucion in Institucion.objects.all():
                # Reemplazar espacios en el nombre de la institución por guiones bajos
                nombre_institucion_limpio = institucion.nombreInstitucion.replace(' ', '_')
                print(f"Procesando institución: {nombre_institucion_limpio}")

                for mes_nombre, mes_num in self.MESES:
                    # Reemplazar espacios en el nombre del mes por guiones bajos (en caso de ser necesario)
                    mes_nombre_limpio = mes_nombre.replace(' ', '_')

                    cuentas_por_cobrar = obtener_cuentas_por_cobrar(institucion.nombreInstitucion, mes_nombre)
                    key = f"cuentas_por_cobrar:{nombre_institucion_limpio}:{mes_nombre_limpio}"
                    print(f"Key: {key}")

                    # Verificar si se obtuvieron cuentas por cobrar
                    logger.info(f"Cuentas por cobrar para {nombre_institucion_limpio} en {mes_nombre_limpio}: {cuentas_por_cobrar}")
                    if cuentas_por_cobrar:  # Solo procede si hay datos
                        # Convertir todos los datos a JSON
                        cuentas_json = json.dumps(cuentas_por_cobrar)  # Convertir a JSON

                        try:
                            # Usar 'ex' en lugar de 'timeout' para establecer la expiración
                            result = r.set(key, cuentas_json, ex=60 * 60 * 24)  # Guardar toda la información por 24 horas
                            print(result)  # Imprimir el resultado de la operación de caché
                            logger.info(f"Guardado en Redis: {key} con datos: {cuentas_json}")
                        except Exception as e:
                            logger.error(f"Error al guardar en Redis: {e}")
                    else:
                        logger.warning(f"No se encontraron cuentas por cobrar para {nombre_institucion_limpio} en {mes_nombre_limpio}.")

        except redis.exceptions.ConnectionError as e:
            print(f"Failed to connect to Redis: {e}")
        self.stdout.write(self.style.SUCCESS('Comando ejecutado con éxito.'))
