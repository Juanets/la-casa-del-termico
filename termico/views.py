from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets

from termico.serializers import ClienteSerializer, ChoferSerializer, ReporteSerializer
from crud.models import Cliente, Chofer
from rutas.models import Reporte

@login_required
def home(request):
    '''Mostrar la landing page, la pagina principal.'''
    return render(request, 'home.html')

@login_required
def ayuda(request):
    '''Mostrar pagina de ayuda.'''
    return render(request, 'ayuda.html')

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class ChoferViewSet(viewsets.ModelViewSet):
    queryset = Chofer.objects.all()
    serializer_class = ChoferSerializer

class ReporteViewSet(viewsets.ModelViewSet):
    queryset = Reporte.objects.all()
    serializer_class = ReporteSerializer