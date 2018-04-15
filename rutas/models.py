from django.db import models

# Create your models here.
class Reporte(models.Model):
    fecha = models.DateField()
    clientes = models.ManyToManyField('crud.Cliente', through='DeliveringOrder')
    chofer = models.ForeignKey('crud.Chofer', on_delete=models.CASCADE)
    distancia = models.CharField(max_length=10)
    duracion = models.CharField(max_length=30)

class DeliveringOrder(models.Model):
    number = models.PositiveIntegerField()
    r = models.ForeignKey(Reporte, on_delete=models.CASCADE)
    c = models.ForeignKey('crud.Cliente', on_delete=models.CASCADE)