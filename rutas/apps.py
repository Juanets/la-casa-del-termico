from django.apps import AppConfig
from watson import search as watson

class RutasConfig(AppConfig):
    name = 'rutas'
    def ready(self):
        Reporte = self.get_model('Reporte')
        watson.register(Reporte)