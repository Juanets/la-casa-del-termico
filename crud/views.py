from crud.models import Cliente

from django.shortcuts import render
from django.core.paginator import Paginator

def clientes_buscar(request):
    clientes = Cliente.objects.all()
    p = Paginator(clientes, 10)

    page = request.GET.get('p')

    if not page:
        page = 1

    page_range = calc_page_range(int(page), p.num_pages)

    return render(request, 'clientes_buscar.html', {'clientes': p.get_page(page), 'paginator': p, 'page_range': page_range})

def calc_page_range(page, num_pages):
    start = page
    end = page + 4

    if end > num_pages:
        diff = end - num_pages
        end = end - diff

    page_range = [i for i in range(start, end+1)]
    return page_range
