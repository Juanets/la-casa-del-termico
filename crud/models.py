from django.db import models

# Create your models here.
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.CharField(blank=True, max_length=60)
    telefono = models.CharField(blank=True, max_length=50)
    colonia = models.CharField(max_length=50)
    calle = models.CharField(max_length=50)
    cp = models.CharField(blank=True, max_length=5)
    numero_int = models.CharField(blank=True, max_length=20)
    numero_ext = models.CharField(blank=True, max_length=20)
    lat = models.CharField(max_length=20)
    lng = models.CharField(max_length=20)
    zona = models.CharField(max_length=6)


class Chofer(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.CharField(blank=True, max_length=70)
    telefono = models.CharField(blank=True, max_length=13)
