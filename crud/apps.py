from django.apps import AppConfig
from watson import search as watson

class CrudConfig(AppConfig):
    name = 'crud'

    # inicializar watson para habilitar la busqueda inteligente
    def ready(self):
        Cliente = self.get_model('Cliente')
        watson.register(Cliente)
