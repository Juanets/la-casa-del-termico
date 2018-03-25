from crud.models import Cliente

from django.shortcuts import render, redirect
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
    print(cliente)
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