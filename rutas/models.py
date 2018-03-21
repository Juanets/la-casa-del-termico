from django.db import models

# Create your models here.
class Reporte(models.Model):
    fecha = models.DateField()
    clientes = models.ManyToManyField('crud.Cliente')
    chofer = models.ForeignKey('crud.Chofer', on_delete=models.CASCADE)
    distancia = models.CharField(max_length=10)
    duracion_int = models.IntegerField()
    duracion_str = models.CharField(max_length=30)
    # warnings[]