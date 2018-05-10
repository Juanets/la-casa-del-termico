from crud.models import Cliente, Chofer
from rutas.models import Reporte
from rest_framework import serializers


class ClienteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


class ChoferSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chofer
        fields = '__all__'


class ReporteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reporte
        fields = '__all__'