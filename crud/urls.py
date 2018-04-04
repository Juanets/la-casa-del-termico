from django.urls import path
from . import views

urlpatterns = [
    path('clientes/', views.clientes_lista, name='clientes_lista'),
    path('clientes/<int:id>/', views.clientes_ver, name='clientes_ver'),
    path('clientes/buscar_handler/', views.clientes_buscar_handler, name='clientes_buscar_handler'),        
    path('clientes/buscar/<str:query>/', views.clientes_buscar, name='clientes_buscar'),
    path('clientes/nuevo/', views.clientes_nuevo, name='clientes_nuevo'),
]
