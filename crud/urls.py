from django.urls import path
from . import views

# estas son las URLs que pueden ser accedidas en el sistema
urlpatterns = [
    path('clientes/', views.clientes_lista, name='clientes_lista'), # lista de clientes
    path('clientes/<int:id>/', views.clientes_ver, name='clientes_ver'), #perfil de cliente
    path('clientes/buscar_handler/', views.clientes_buscar_handler, name='clientes_buscar_handler'), # redireccionamiento de busqueda
    path('clientes/buscar/<str:query>/', views.clientes_buscar, name='clientes_buscar'), # busqueda de cliente
    path('clientes/nuevo/', views.clientes_nuevo, name='clientes_nuevo'), # crear cliente
    path('clientes/editar/<int:id>/', views.clientes_editar, name='clientes_editar'), # modificar cliente
    path('clientes/borrar/<int:id>/', views.clientes_borrar, name='clientes_borrar'), # borrar cliente
]
