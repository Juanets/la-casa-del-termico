from django.shortcuts import render

from crud.models import Cliente
from .route_helper_functions import *

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


from django.conf import settings
from easy_pdf.views import PDFTemplateView

class HelloPDFView(PDFTemplateView):
    template_name = 'pdf.html'

    # base_url = 'file://' + settings.STATIC_ROOT
    download_filename = 'hello.pdf'

    def get_context_data(self, **kwargs):
        return super(HelloPDFView, self).get_context_data(
            pagesize='A4',
            title='Hi there!',
            **kwargs
        )