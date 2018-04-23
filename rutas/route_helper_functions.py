import datetime
import time

from django.db.models import Case, When
from crud.models import Cliente
import googlemaps

# inicializar API de Maps
gmaps = googlemaps.Client(key='AIzaSyCqwRVeYfYRGF8qsROpKoCyYDWqmUJDGHo')

# traducciones de meses
months = {
        'January': 'Enero',
        'February': 'Febrero',
        'March': 'Marzo',
        'April': 'Abril',
        'May': 'Mayo',
        'June': 'Junio',
        'July': 'Julio',
        'August': 'Agosto',
        'September': 'Septiembre',
        'October': 'Octubre',
        'November': 'Noviembre',
        'December': 'Diciembre'        
    }

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

def locale_date(date):
    # obtener el mes en idioma español
    en_month = date.strftime('%B')
    es_month = months[en_month]

    # escribir fecha completa en forma de texto en español
    fecha = date.strftime('%d de {mes} del %Y, %H:%M %p').format(mes=es_month)

    return fecha
