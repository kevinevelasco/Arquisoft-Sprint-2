# Generated by Django 5.1.1 on 2024-10-05 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manejador_reportes', '0002_detallecobrocurso_detallecobroestudiante_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DetalleCobroCurso',
        ),
        migrations.DeleteModel(
            name='DetalleCobroEstudiante',
        ),
    ]