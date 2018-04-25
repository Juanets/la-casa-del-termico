from django.urls import path
from . import views

# estas son las URLs que pueden ser accedidas en el sistema
urlpatterns = [
    path('clientes/', views.clientes_lista, name='clientes_lista'), # lista de clientes
    path('clientes/<int:id>/', views.clientes_ver, name='clientes_ver'), #perfil de cliente
    path('clientes/buscar_handler/', views.clientes_buscar_handler, name='clientes_buscar_handler'), # redireccionamiento de busqueda
    path('clientes/buscar/<str:query>/', views.clientes_buscar, name='clientes_buscar'), # busqueda de cliente
    path('clientes/nuevo/', views.clientes_nuevo, name='clientes_nuevo'), # crear cliente
    path('clientes/<int:id>/editar/', views.clientes_editar, name='clientes_editar'), # modificar cliente
    path('clientes/<int:id>/borrar/', views.clientes_borrar, name='clientes_borrar'), # borrar cliente
    path('clientes/mapa/', views.clientes_mapa, name='clientes_mapa'), # visualizar todos los clientes en el mapa de Hermosillo
    path('choferes/', views.choferes_ver, name='choferes'), # ver choferes 
    path('chofer/nuevo/', views.chofer_nuevo, name='chofer_nuevo'), # crear nuevo chofer
    path('chofer/<int:id>/editar/', views.chofer_editar, name='chofer_editar'), # editar chofer
    path('chofer/<int:id>/borrar/', views.chofer_borrar, name='chofer_borrar'), # borrar chofer    
]
