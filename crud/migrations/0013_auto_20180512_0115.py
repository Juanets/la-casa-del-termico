# Generated by Django 2.0.3 on 2018-05-12 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0012_auto_20180512_0110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='cp',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
