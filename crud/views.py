from crud.models import Cliente
from crud.forms import ClienteForm

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from watson import search as watson

def clientes_lista(request):
    clientes = Cliente.objects.all()
    p = Paginator(clientes, 10)

    page = request.GET.get('p')

    if not page:
        page = 1

    page_range = calc_page_range(int(page), p.num_pages)

    return render(request, 'clientes_lista.html', {'clientes': p.get_page(page), 'paginator': p, 'page_range': page_range})

def calc_page_range(page, num_pages):
    '''
        Calcular de qué página a qué página se mostrará el menu paginador.
        Ejemplo: si estas en la página 2, el paginador será de [2, 3, 4, 5, 6]
    '''
    start = page
    end = page + 4

    if end > num_pages:
        diff = end - num_pages
        end = end - diff

    page_range = [i for i in range(start, end+1)]
    return page_range

def clientes_ver(request, id):
    cliente = Cliente.objects.get(id=id)

    return render(request, 'clientes_ver.html', {'c': cliente})

def clientes_buscar_handler(request):
    query = request.GET.get('query')
    return redirect(clientes_buscar, query=query)

def clientes_buscar(request, query):
    # query = request.GET.get('query')

    search_results = watson.filter(Cliente, query)

    if not search_results:
        return render(request, 'buscar_404.html', {'query': query})

    p = Paginator(search_results, 10)

    page = request.GET.get('p')

    if not page:
        page = 1

    page_range = calc_page_range(int(page), p.num_pages)
    print(type(p.num_pages))
    return render(request, 'clientes_lista.html', {'clientes': p.get_page(page), 'paginator': p, 'page_range': page_range, 'query': query})

def clientes_nuevo(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            nuevo = Cliente()
            nuevo.nombre = form.cleaned_data['nombre']
            nuevo.telefono = form.cleaned_data['telefono']
            nuevo.colonia = form.cleaned_data['colonia']
            nuevo.calle = form.cleaned_data['calle']
            nuevo.numero_int = form.cleaned_data['numero_int']
            nuevo.numero_ext = form.cleaned_data['numero_ext']
            nuevo.cp = form.cleaned_data['cp']
            nuevo.lat = form.cleaned_data['lat']
            nuevo.lng = form.cleaned_data['lng']
            if form.cleaned_data['zona'] == 1:
                nuevo.zona = 'Norte'
            else:
                nuevo.zona = 'Sur'
            if form.cleaned_data['correo']:
                nuevo.correo = form.cleaned_data['correo']
            else:
                nuevo.correo = 'Sin correo'                

            nuevo.save()

            success = '''Cliente <i>{cliente}</i> creado con éxito. <a href="/clientes/nuevo" 
            class="alert-link">¿Crear otro?</a>'''.format(cliente=nuevo.nombre)

            return render(request, 'clientes_ver.html', {'c': nuevo, 'messages': success})
            
    else:
        form = ClienteForm()      
        return render(request, 'clientes_nuevo.html', {'form': form})
