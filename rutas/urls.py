from django.urls import path
from . import views

urlpatterns = [
    path('rutas/nueva/', views.generar_ruta, name='rutas_nueva'),  
    path('rutas/asdf', views.asdf, name='asdf'),
    path('rutas/guardar/', views.guardar_ruta, name='rutas_guardar'),
    path('reportes/<int:id>/', views.reporte_ver, name='reporte_ver'),  
    path('reportes/Reporte <int:id> - <str:fecha>.pdf', views.reporte_pdf, name='reporte_pdf'),    
]
