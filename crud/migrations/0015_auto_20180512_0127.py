# Generated by Django 2.0.3 on 2018-05-12 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0014_auto_20180512_0120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='correo',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='cp',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='numero_ext',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='numero_int',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefono',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
