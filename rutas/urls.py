from django.urls import path
from . import views

urlpatterns = [
    path('rutas/nueva/', views.generar_ruta, name='rutas_nueva'),  
    path('rutas/asdf', views.asdf, name='asdf'),
    path('rutas/guardar/', views.guardar_ruta, name='rutas_guardar'),    
    path('reporte-<int:id>.pdf', views.pdf, name='pdf'),    
]
