# Generated by Django 2.0.3 on 2018-04-18 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rutas', '0004_reporte_clientes'),
    ]

    operations = [
        migrations.AddField(
            model_name='reporte',
            name='mapa_url',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
    ]
