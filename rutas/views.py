from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import get_template 

from watson import search as watson
import pdfkit
import datetime
import time

from crud.models import Cliente, Chofer
from rutas.models import Reporte, DeliveringOrder
from .route_helper_functions import *

def generar_ruta(request):
    '''Funcion para generar ruta optima usando la API de Google Maps.'''
    if request.method == 'POST':

        # posicion en la lista de los clientes priorizados
        prioritize_index = request.POST.getlist('prioritize')

        # lista de IDs de clientes seleccionados (con espacios vacios y nulos)
        dirty_selected_clients = [request.POST.get(str(i)) for i in range(1, 24)]
    
        # IDs de TODOS los clientes seleccionados (lista limpia)
        selected_clients = list(filter(None, dirty_selected_clients))
        
        # obtener datos de TODOS los clientes seleccionados por medio de su ID
        client_objs = get_clients_by_order(selected_clients)

        # obtener coordenadas de los clientes en un formato separado por comas 'lat,lng'
        client_coordinates = [{'id': c.id, 'coord': '{lat},{lng}'.format(lat=c.lat, lng=c.lng)} for c in client_objs]

        # si el usuario marcó que hay clientes priorizados...
        if prioritize_index:            
            # IDs y coordenadas de SOLO los clientes priorizados
            prioritized_clients = [client_coordinates[int(c)-1] for c in prioritize_index]

            # IDs y coordenadas de SOLO los clientes no priorizados
            not_prioritized_clients = subtract_client_list(client_coordinates, prioritized_clients)

            # si TODOS los clientes estan priorizados...
            if not not_prioritized_clients:

                # orden final de la ruta
                # sera exactamente igual al orden introducido
                final_client_order = prioritized_clients

                # no se optimizará la ruta ya que se tiene que
                # obedecer el orden de los clientes priorizados
                optimize = False

                # datos de la ruta final (tiempo, distancia, orden) para guardar en BD
                final_route_data = calculate_route(final_client_order, optimize=optimize) 

            # si sí hay clientes no priorizados (en conjunto con clientes que sí lo están)
            else:
                # obtener orden optimo para los clientes no priorizados 
                optimal_route_data = calculate_route(not_prioritized_clients, optimize=True)
                optimized_client_order = [not_prioritized_clients[i] for i in optimal_route_data['waypoint_order']]
                
                # orden final de la ruta
                for i, p_index in enumerate(prioritize_index):
                    optimized_client_order.insert(int(p_index)-1, prioritized_clients[i])
                
                final_client_order = optimized_client_order

                # datos finales de la ruta
                final_route_data = calculate_route(final_client_order, optimize=False)         
                
        # si no hay priorizados, el orden no importa por lo tanto...            
        else:
            # como el orden no importa, es mejor que optimicemos la ruta
            optimize = True

            # datos de la ruta final (tiempo, distancia, orden) para guardar en BD
            final_route_data = calculate_route(client_coordinates, optimize=optimize)

            # orden de entrega optimo
            optimal_waypoint_order = final_route_data['waypoint_order']
            final_client_order = [client_coordinates[i] for i in optimal_waypoint_order]
            
        # obtener el tiempo total de la ruta
        final_route_data['duration'] = calculate_route_time(final_route_data)

        # obtener distancia total 
        calculate_route_distance(final_route_data)
        final_route_data['distance'] = calculate_route_distance(final_route_data)

        # orden final de las coordenadas, para utilizar en la URL de `iframe_url`
        final_coordinates = [client['coord'] for client in final_client_order]

        # reordenar objetos de cliente
        final_client_objs_order = [c['id'] for c in final_client_order]
        client_objs = get_clients_by_order(final_client_objs_order)

        # generar URL para el mapa en HTML
        iframe_url = (
                        'https://www.google.com/maps/embed/v1/directions?'
                        'key=AIzaSyCqwRVeYfYRGF8qsROpKoCyYDWqmUJDGHo'
                        '&origin=la+casa+del+termico'
                        '&destination=la+casa+del+termico'
                        '&waypoints={wp}'.format(wp='|'.join(final_coordinates))
                    )

        # obtener lista de choferes existentes
        choferes = Chofer.objects.all()
        return render(request,'rutas_mapa_generado.html', {
                                                    'iframe_url': iframe_url,
                                                    'clientes': client_objs,
                                                    'route': final_route_data,
                                                    'choferes': choferes,
                                                    'fecha': datetime.datetime.now()
                                                }
                                            )

def escoger_clientes(request):
    '''Funcion para que el usuario escoja los clientes de la ruta.'''

    # obtener todos los clientes
    c = Cliente.objects.all()

    # renderear la seccion de escoger clientes para ruta
    return render(request, 'rutas_escoger_clientes.html', {'c':c, 'range': range(1, 24)})


def guardar_ruta(request):
    '''Funcion para guardar ruta en la base de datos.'''
    # si el request es POST
    if request.method == 'POST':
        fecha = datetime.datetime.now() # fecha 
        clientes = get_clients_by_order(request.POST.getlist('ids')) # lista de clientes
        chofer = Chofer.objects.get(id=request.POST.get('chofer')) # chofer de la ruta
        duracion = request.POST.get('duracion') # duracion de la ruta
        distancia = request.POST.get('distancia') # distancia total en km
        mapa_url = request.POST.get('iframe_url') # URL de maps para visualizar la ruta

        # creamos el reporte y guardamos
        r = Reporte(
                    fecha=fecha,
                    fecha_str=locale_date(fecha),
                    chofer=chofer,
                    chofer_nombre=chofer.nombre,
                    duracion=duracion,
                    distancia=distancia,
                    mapa_url=mapa_url,
                )

        r.save()
        
        # guardar clientes en orden de entrega
        for i, c in enumerate(clientes):
            DeliveringOrder.objects.create(r=r, c=c, number=i)
        
        r.save()

        # una vez guardada la ruta, mostrar el reporte en una nueva pestaña
        return redirect(reporte_ver, id=r.id)


def reportes_lista(request):
    '''Funcion para mostrar una tabla de todos los reportes guardados.'''

    # obtenemos todos los reportes
    reportes = Reporte.objects.all()

    # si aun no hay reportes, se le indica al usuario
    if not reportes:
        return render(request, 'reportes_lista_vacio.html')

    # paginacion
    p = Paginator(reportes, 10)
    page = request.GET.get('p')
    if not page:
        page = 1
        
    page_range = calc_page_range(int(page), p.num_pages)

    # renderear la lista de reportes
    return render(request, 'reportes_lista.html', {'reportes': p.get_page(page), 'paginator': p, 'page_range': page_range})

def reporte_buscar_handler(request):
    '''Funcion para obtener el termino de busqueda y redireccionar a la busqueda.'''    
    query = request.GET.get('query')
    
    return redirect(reporte_buscar, query=query)

def reporte_buscar(request, query):
    '''Funcion para filtrar reportes por chofer, tiempo, fecha o distancia.'''

    # usamos la libreria `watson` para filtrar los clientes de acuerdo a la query de busqueda    
    search_results = watson.filter(Reporte, query)

    # si no hay resultados de busqueda, se le indicara al cliente
    if not search_results:
        section = 'reportes'
        return render(request, 'buscar_404.html', {'query': query, 'section': section})

    # mostramos hasta 10 reusltados por pagina
    p = Paginator(search_results, 10)
    page = request.GET.get('p')
    if not page:
        page = 1

    page_range = calc_page_range(int(page), p.num_pages)

    # finalmente mostramos los resultados al usuario
    return render(request, 'reportes_lista.html', {'reportes': p.get_page(page), 'paginator': p, 'page_range': page_range, 'query': query})

def reporte_ver(request, id):
    '''Funcion para ver un reporte en especifico.'''

    # obtenemos el reporte que se quiere ver
    reporte = Reporte.objects.get(id=id)

    # estos son los clientes involucrados en la ruta de entrega
    clientes = reporte.clientes.all()

    return render(request, 'reportes_ver.html', {'reporte': reporte, 'clientes': clientes})

def reportes_borrar(request, id):
    '''Funcion para borrar un reporte.'''

    # esta funcion solo es accesible a traves de un metodo POST    
    if request.method == 'POST':
        reporte = Reporte.objects.get(id=id)
        reporte.delete()
        # despues de borrar se le redirige al usuario a la lista de todos los reportes
        return redirect(reportes_lista)

    # si se quiere acceder a traves de GET, se redirigira al perfil del cliente
    # esto se hace como una medida de seguridad
    # (no se debe alterar informacion a traves de requests tipo GET)        
    else:
        return redirect(reporte_ver, id=id)

def reportes_chofer(request, id):
    '''Funcion para ver la lista de entregas que ha hecho un chofer.'''

    # obtener el chofer que se quiere ver
    chofer = Chofer.objects.get(id=id)
    
    # consultar reportes de dicho chofer
    reportes = Reporte.objects.filter(chofer=chofer)

    # si el chofer no tiene entregas (reportes)
    # rendereamos que le indica eso mismo al usuario
    if not reportes:
        return render(request, 'reportes_lista_chofer_vacio.html', {'chofer':chofer})

    # paginador, rango de pagindaor, etc
    p = Paginator(reportes, 10)
    page = request.GET.get('p')
    if not page:
        page = 1

    page_range = calc_page_range(int(page), p.num_pages)

    # renderear una lista de reportes del chofer
    return render(request, 'reportes_lista_chofer.html', {
                                                            'reportes': p.get_page(page),
                                                            'chofer': chofer, 
                                                            'paginator': p, 
                                                            'page_range': page_range
                                                        }
                                                    )

def reporte_pdf(request, id, fecha):

    template = get_template('pdf.html')

    # obtener el reporte que se quiere ver 
    r = Reporte.objects.get(id=id)
    context = r.__dict__

    # obtener clientes y chofer de la entrega
    context['clientes'] = r.clientes.all()
    context['chofer'] = r.chofer.nombre

    html = template.render(context)

    options = {
        'margin-top': '20mm',
        'margin-right': '20mm',
        'margin-bottom': '20mm',
        'margin-left': '20mm',
        'javascript-delay': 1000,

    }

    pdf = pdfkit.from_string(html, False, options=options)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="somefilename.pdf"'

    return response
