from django.shortcuts import render
from django.db.models import Case, When

from crud.models import Cliente
import googlemaps

from pprint import pprint
import datetime
import time

# inicializar API de Maps
gmaps = googlemaps.Client(key='AIzaSyCqwRVeYfYRGF8qsROpKoCyYDWqmUJDGHo')

def generar_ruta(request):
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

        return render(request, 'rutas_mapa_generado.html', {'iframe_url': iframe_url, 'clientes': client_objs, 'route': final_route_data})

def asdf(request):
    c = Cliente.objects.all()

    return render(request, 'asdf.html', {'c':c, 'range': range(1, 24)})

def calculate_route(client_list, optimize=False):

    # obtenemos las puras coordenadas del diccionario `client_list`
    coordinates = [client['coord'] for client in client_list]

    # hacer request a la API de directions
    directions_result = gmaps.directions(
                                mode='driving',
                                language='es',
                                units='metric',
                                origin='la casa del termico',
                                destination='la casa del termico',
                                optimize_waypoints=optimize,
                                waypoints=coordinates,
                        )

    return directions_result[0]

def calculate_route_time(route):
    # etapas de la ruta (cada `leg` es la ruta de un punto a otro)
    legs = route['legs']

    # sumar los segundos de cada etapa para calcular el tiempo total
    duration_seconds = sum([leg['duration']['value'] for leg in legs])
    
    # dar formato al tiempo (e.g. '10 h 27 min')
    duration = time.strftime('%H h %M min', time.gmtime(duration_seconds))
    duration = ' '.join([s.lstrip('0') for s in duration.split()])

    # si la ruta dura menos de una hora hay que eliminar la 'h' 
    # e.g. ' h 36 min' -> '36 min'
    if duration[0] == ' ':
        duration = duration[3:]
    
    return duration

def calculate_route_distance(route):
    # etapas de la ruta (cada `leg` es la ruta de un punto a otro)
    legs = route['legs']

    # sumar la distancia en metros de cada etapa
    distance_meters = sum([leg['distance']['value'] for leg in legs])
    
    # metros a kilometros (e.g. '31.3 km')
    distance = '{d} km'.format(d=round(distance_meters/1000,1))

    return distance

def subtract_client_list(parent, child):
    # funcion para quitar lista de clientes priorizados
    # de la lista de clientes completa
    # para obtener la lista de los no priorizados
    parent_hashable = (frozenset(x.items()) for x in parent)
    child_hashable = (frozenset(x.items()) for x in child)

    diff = set(parent_hashable).difference(child_hashable)

    return [dict(x) for x in diff]

def get_clients_by_order(clients):
    # preservar orden al hacer el filtrado en la base de datos 
    # i.e: .order_by(preserved)
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(clients)])

    return Cliente.objects.filter(pk__in=clients).order_by(preserved)