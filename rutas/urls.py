from django.urls import path
from . import views

urlpatterns = [
    path('rutas/resultado/', views.generar_ruta, name='rutas_resultado'),  
    path('rutas/nueva/', views.escoger_clientes, name='rutas_nueva'),
    path('rutas/guardar/', views.guardar_ruta, name='rutas_guardar'),
    path('reportes/<int:id>/', views.reporte_ver, name='reporte_ver'),  
    path('reportes/Reporte <int:id> - <str:fecha>.pdf', views.reporte_pdf, name='reporte_pdf'), 
    path('reportes/buscar_handler/', views.reporte_buscar_handler, name='reporte_buscar_handler'),
    path('reportes/buscar/<str:query>/', views.reporte_buscar, name='reporte_buscar'),
    path('reportes/', views.reportes_lista, name='reportes_lista'),
    path('reportes/borrar/<int:id>/', views.reportes_borrar, name='reportes_borrar'),
    path('chofer/<int:id>/entregas/', views.reportes_chofer, name='reportes_chofer'),    
]
