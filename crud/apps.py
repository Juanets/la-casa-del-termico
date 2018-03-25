from django.apps import AppConfig
from watson import search as watson

class CrudConfig(AppConfig):
    name = 'crud'
    def ready(self):
        Cliente = self.get_model('Cliente')
        watson.register(Cliente)
