from django import forms
from crud.models import Cliente

ZONA_CHOICES = (('1', 'Norte',), ('2', 'Sur',))

class ClienteForm(forms.ModelForm):
    zona = forms.ChoiceField(
        choices=(ZONA_CHOICES),
        widget=forms.Select(),
    )
    
    class Meta:
        model = Cliente
        fields = '__all__'

class ChoferForm(forms.ModelForm):    
    class Meta:
        model = Chofer
        fields = '__all__'