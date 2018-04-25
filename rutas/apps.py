from django.apps import AppConfig
from watson import search as watson

# configuracion de la app
class RutasConfig(AppConfig):
    name = 'rutas'

    # inicializamos el buscador inteligente `watson`
    def ready(self):
        Reporte = self.get_model('Reporte')
        watson.register(Reporte)