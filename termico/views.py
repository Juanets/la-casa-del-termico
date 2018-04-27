from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    '''Mostrar la landing page, la pagina principal.'''
    return render(request, 'home.html')

@login_required
def ayuda(request):
    '''Mostrar pagina de ayuda.'''
    return render(request, 'ayuda.html')
