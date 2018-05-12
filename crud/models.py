from django.db import models

# modelos de base de datos
# aqui se crean las entidades de la base de datos y sus campos (y el tipo de campos)
class Cliente(models.Model):
    '''Campos del cliente.'''
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(blank=True)
    telefono = models.CharField(max_length=50, blank=True)
    colonia = models.CharField(max_length=100)
    calle = models.CharField(max_length=100)
    cp = models.IntegerField(blank=True)
    numero_int = models.CharField(blank=True, max_length=20)
    numero_ext = models.CharField(blank=True, max_length=20)
    lat = models.DecimalField(max_digits=25, decimal_places=20)
    lng = models.DecimalField(max_digits=25, decimal_places=20)
    zona = models.CharField(max_length=6)


class Chofer(models.Model):
    '''Campos del chofer.'''
    nombre = models.CharField(max_length=50)
    correo = models.EmailField()
    telefono = models.IntegerField()
