from django.urls import path
from . import views

# URLs accesibles que tienen que ver con las rutas y reportes
urlpatterns = [
    path('rutas/nueva/', views.escoger_clientes, name='rutas_nueva'), # escoger clientes para la ruta    
    path('rutas/resultado/', views.generar_ruta, name='rutas_resultado'), # ruta generada
    path('rutas/guardar/', views.guardar_ruta, name='rutas_guardar'), # guardar una ruta
    path('reportes/<int:id>/', views.reporte_ver, name='reporte_ver'),  # ver un reporte en espcifico
    path('reportes/Reporte <int:id> - <str:fecha>.pdf', views.reporte_pdf, name='reporte_pdf'), # ver el PDF del reporte
    path('reportes/buscar_handler/', views.reporte_buscar_handler, name='reporte_buscar_handler'), # # redireccionamiento de busqueda
    path('reportes/buscar/<str:query>/', views.reporte_buscar, name='reporte_buscar'), # busqueda de reportes
    path('reportes/', views.reportes_lista, name='reportes_lista'), # ver todos los reportes
    path('reportes/borrar/<int:id>/', views.reportes_borrar, name='reportes_borrar'), # borrar un reporte
    path('chofer/<int:id>/entregas/', views.reportes_chofer, name='reportes_chofer'), # ver las entregas (reportes) de un chofer
]
