from django import forms
from crud.models import Cliente, Chofer

# opciones de zona
ZONA_CHOICES = (('1', 'Norte',), ('2', 'Sur',))

# formulario de creacion de cliente
# se hace a partir del modelo de base de datos del cliente
# es decir, el formulario sera para llenar todos los campos del cliente
class ClienteForm(forms.ModelForm):

    # inicializamos el campo de zona
    zona = forms.ChoiceField(
        choices=(ZONA_CHOICES),
        widget=forms.Select(),
    )

    class Meta:
        # indicamos que el modelo sera el de Cliente
        model = Cliente
        fields = '__all__'

class ChoferForm(forms.ModelForm):    
    class Meta:
        model = Chofer
        fields = '__all__'