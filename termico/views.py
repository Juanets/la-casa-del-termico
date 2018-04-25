from django.shortcuts import render

def home(request):
    '''Mostrar la landing page, la pagina principal.'''
    return render(request, 'home.html')