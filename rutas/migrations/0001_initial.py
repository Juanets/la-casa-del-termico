# Generated by Django 2.0.3 on 2018-03-21 01:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('crud', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reporte',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('distancia', models.CharField(max_length=10)),
                ('duracion_int', models.IntegerField()),
                ('duracion_str', models.CharField(max_length=30)),
                ('chofer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crud.Chofer')),
                ('clientes', models.ManyToManyField(to='crud.Cliente')),
            ],
        ),
    ]
