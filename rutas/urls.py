from django.urls import path
from . import views

urlpatterns = [
    path('rutas/nueva/', views.generar_ruta, name='rutas_nueva'),  
    path('rutas/asdf', views.asdf, name='asdf'),      
]

