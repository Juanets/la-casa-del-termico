from django.urls import path
from . import views

urlpatterns = [
    path('clientes/', views.clientes_buscar, name='clientes_buscar'),
    path('clientes/<int:id>', views.clientes_ver, name='clientes_ver'),
]
