# Generated by Django 5.1.1 on 2024-10-06 00:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manejador_cronogramas', '0005_detallecobrocurso_detallecobroestudiante'),
        ('manejador_facturacion', '0002_facturaelectronica_pagoproforma_recibocobro_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recibocobro',
            name='pago',
        ),
        migrations.AddField(
            model_name='pagoproforma',
            name='recibo_cobro',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='manejador_facturacion.recibocobro'),
        ),
        migrations.AddField(
            model_name='recibocobro',
            name='detalles_cobro',
            field=models.ManyToManyField(related_name='recibos', to='manejador_cronogramas.detallecobrocurso'),
        ),
    ]