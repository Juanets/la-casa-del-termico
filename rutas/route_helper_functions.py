import datetime
import time

from django.db.models import Case, When
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template 

from crud.models import Cliente
import googlemaps

# inicializar API de Maps
gmaps = googlemaps.Client(key=settings.MAPS_API_KEY)

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
                                origin='29.124909,-110.964523',
                                destination='29.124909,-110.964523',
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
    '''
        Funcion para quitar lista de clientes priorizados
        de la lista de clientes completa
        para obtener la lista de los no priorizados.
    '''

    # convertimos listas a hashable para poder aplicarles la funcion `set()`
    parent_hashable = (frozenset(x.items()) for x in parent)
    child_hashable = (frozenset(x.items()) for x in child)

    # obtenemos la diferencia entre las dos listas
    diff = set(parent_hashable).difference(child_hashable)

    # regresamos una lista de dicts
    return [dict(x) for x in diff]

def get_clients_by_order(clients):
    '''
        Funcion para preservar orden al hacer el filtrado en la base de datos.
        i.e: .order_by(preserved)
        Se usara para obtener clientes de acuerdo a su prioridad.
    '''
    # hacemos uso de la funcion `Case` de Django 
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(clients)])

    # hacemos la consulta a la base de datos y ordenamos por `preserved`
    return Cliente.objects.filter(pk__in=clients).order_by(preserved)

def locale_date(date):
    '''Funcion para dar formato humano (y en español) a las fechas.'''
    
    # obtener el mes en idioma español
    en_month = date.strftime('%B')
    es_month = months[en_month]

    # escribir fecha completa en forma de texto en español
    fecha = date.strftime('%d de {mes} del %Y, %H:%M %p').format(mes=es_month)

    return fecha

def calc_page_range(page, num_pages):
    '''
        Calcular de qué página a qué página se mostrará el menu paginador.
        Ejemplo: si estas en la página 2, el paginador será de [2, 3, 4, 5, 6]
    '''

    # pagina inicial (e.g. 2)
    start = page

    # pagina final (e.g. 6)
    # en otras palabras, hasta qué página se mostrara
    end = page + 4

    # la suma anterior no puede ser mayor al numero de paginas total
    if end > num_pages:
        # sacamos la diferencia de rango
        diff = end - num_pages
        end = end - diff

    # creamos un arreglo a partir del inicio y final de las paginas
    # e.g si start=2 y end=6 entonces page_range=[2, 3, 4, 5, 6]
    page_range = [i for i in range(start, end+1)]

    # regresamos el rango de paginas
    return page_range

def enviar_ruta_a_chofer(chofer, route_str):
    '''Enviar correo al chofer con enlace de la ruta, para que pueda verla él mismo.'''

    # coordenadas de la bodega de la casa del termico  
    base = '/29.124909,-110.964523/'

    # editar la URL de la ruta que se guardó en la base de datos.
    # la que se guarda en base de datos no la puede ver directamente el chofer,
    # hay que reemplazar partes de la URL para que la ruta sea publica
    waypoints = base + route_str[165:].replace('|', '/') + base
    route_url = 'https://www.google.com/maps/dir' + waypoints

    # contexto para la template
    context = {
        'url': route_url,
        'nombre': chofer.nombre
    }

    # asunto
    subject = 'Ruta de entrega - La Casa del Térmico'

    # renderear la template html (este es el mensaje que se enviara)
    content = get_template('rutas_email.html').render(context)

    # enviar mensaje por correo, en forma de html
    msg = EmailMultiAlternatives(subject, content, settings.EMAIL_HOST_USER, [chofer.correo])
    msg.content_subtype = 'html'
    msg.send()
