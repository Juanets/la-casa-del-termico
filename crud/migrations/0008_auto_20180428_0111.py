# Generated by Django 2.0.3 on 2018-04-28 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0007_auto_20180425_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='calle',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='colonia',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefono',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
