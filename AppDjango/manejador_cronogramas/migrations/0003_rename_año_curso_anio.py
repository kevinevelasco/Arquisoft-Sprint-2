# Generated by Django 5.1.1 on 2024-10-05 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manejador_cronogramas', '0002_cronogramabase_cronogramaestudiante_curso_descuento_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='curso',
            old_name='año',
            new_name='anio',
        ),
    ]
