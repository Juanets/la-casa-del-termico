from django.db import models

# Create your models here.
class Reporte(models.Model):
    fecha = models.DateField()
    fecha_str = models.CharField(max_length=50)
    clientes = models.ManyToManyField('crud.Cliente', through='DeliveringOrder')
    chofer = models.ForeignKey('crud.Chofer', on_delete=models.CASCADE)
    chofer_nombre = models.CharField(max_length=100)
    distancia = models.CharField(max_length=10)
    duracion = models.CharField(max_length=30)
    mapa_url = models.CharField(max_length=500)


class DeliveringOrder(models.Model):
    number = models.PositiveIntegerField()
    r = models.ForeignKey(Reporte, on_delete=models.CASCADE)
    c = models.ForeignKey('crud.Cliente', on_delete=models.CASCADE)