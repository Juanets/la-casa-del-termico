from crud.models import Cliente
from crud.forms import ClienteForm 
from crud.models import Chofer
from crud.forms import ChoferForm

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from watson import search as watson
from rutas.route_helper_functions import calc_page_range

def clientes_lista(request):
    '''Funcion para mostrar la lista de todos clientes como tabla.'''

    # hacemos la consulta a la base de datos
    clientes = Cliente.objects.all()

    # hacemos la paginacion, para mostrar 10 clientes por pagina
    p = Paginator(clientes, 10)

    # obtenemos la pagina que se quiere ver a traves del parametro `p`
    # e.g. /clientes/?p=3
    # si no existe tal parametro, significa que la pagina es la primera (1)
    page = request.GET.get('p')
    if not page:
        page = 1

    # calculamos el rango de paginas que se mostrara en el menu, a partir de la pagina actual
    page_range = calc_page_range(int(page), p.num_pages)

    # rendereamos los clientes
    return render(request, 'clientes_lista.html', {'clientes': p.get_page(page), 'paginator': p, 'page_range': page_range})

def clientes_ver(request, id):
    '''Funcion para mostrar el perfil de un cliente en especifico.'''

    # hacemos la conslta a la base de datos, obtenemos el cliente a partir de su ID
    cliente = Cliente.objects.get(id=id)

    # rendereamos dicho cliente usando la template `clientes_ver.html`
    return render(request, 'clientes_ver.html', {'c': cliente})

def clientes_buscar_handler(request):
    '''Funcion para obtener el termino de busqueda y redireccionar a la busqueda.'''

    # obtenemos el parametro `query` desde la URl
    # e.g. /clientes/buscar/?query=jesus
    query = request.GET.get('query')

    # redireccionamos para hacer la busqueda
    return redirect(clientes_buscar, query=query)

def clientes_buscar(request, query):
    '''Buscar clientes a partir de su nombre, direccion, telefono, correo...'''

    # usamos la libreria `watson` para filtrar los clientes de acuerdo a la query de busqueda
    search_results = watson.filter(Cliente, query)

    # si no existen resultados para dicha query...
    if not search_results:

        # rendereamos `buscar_404.html` para decirle al usuario que su busqueda no dio resultado
        section = 'clientes'
        return render(request, 'buscar_404.html', {'query': query, 'section': section})

    # si hubo resultados, creamos un paginador para mostrar hasta 10 resultados por busqueda
    p = Paginator(search_results, 10)

    page = request.GET.get('p')
    if not page:
        page = 1

    page_range = calc_page_range(int(page), p.num_pages)

    # mostramos la lista de clientes filtrados
    return render(request, 'clientes_lista.html', {'clientes': p.get_page(page), 'paginator': p, 'page_range': page_range, 'query': query})

def clientes_nuevo(request):
    '''Funcion para crear un nuevo cliente.'''

    # si la request que se hizo a `clientes/nuevo/` es de tipo POST
    # i.e. si se quiere meter nueva informacion (crear nuevo cliente)
    if request.method == 'POST':
        
        # llenamos el formulario con la informacion que introdujo el usuario
        # y lo validamos
        form = ClienteForm(request.POST)
        if form.is_valid():
            # si los datos son validos
            # creamos el cliente y llenamos cada dato
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

            # si la zona es `1` entonces es zona Norte, 
            # si es `2` sera Sur
            if form.cleaned_data['zona'] == 1:
                nuevo.zona = 'Norte'
            else:
                nuevo.zona = 'Sur'
            if form.cleaned_data['correo']:
                nuevo.correo = form.cleaned_data['correo']
            else:
                nuevo.correo = 'Sin correo'                

            # guardamos al cliente en la base de datos
            nuevo.save()

            # creamos el mensaje de exito, el cual se mostrara al usuario
            # para hacerle saber que el cliente se creo con exito
            success = '''Cliente <i>{cliente}</i> creado con éxito. <a href="/clientes/nuevo" 
            class="alert-link">¿Crear otro?</a>'''.format(cliente=nuevo.nombre)

            # una vez creado, mostramos el perfil del cliente creado y anexamos el mensaje de exito
            return render(request, 'clientes_ver.html', {'c': nuevo, 'messages': success})

    # si el tipo de request que se hizo es te tipo GET...            
    else:
        # obtenemos el formulario de creacion de cliente y lo rendereamos
        # para que el usuario lo llene
        form = ClienteForm()      
        return render(request, 'clientes_nuevo.html', {'form': form})

def clientes_editar(request, id):
    '''Funcion para editar un cliente existente.'''

    # primero obtenemos el id del cliente que se va a editar
    cliente = Cliente.objects.get(id=id)

    # si el tipo de request que se hizo a `/clientes/<id>/editar/` es POST...
    if request.method == 'POST':
        # se valida la informacion y se actualiza el cliente, 
        # igual a como se hace cuando se crea un nuevo cliente
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente.nombre = form.cleaned_data['nombre']
            cliente.telefono = form.cleaned_data['telefono']
            cliente.colonia = form.cleaned_data['colonia']
            cliente.calle = form.cleaned_data['calle']
            cliente.numero_int = form.cleaned_data['numero_int']
            cliente.numero_ext = form.cleaned_data['numero_ext']
            cliente.cp = form.cleaned_data['cp']
            cliente.lat = form.cleaned_data['lat']
            cliente.lng = form.cleaned_data['lng']
            if form.cleaned_data['zona'] == 1:
                cliente.zona = 'Norte'
            else:
                cliente.zona = 'Sur'
            if form.cleaned_data['correo']:
                cliente.correo = form.cleaned_data['correo']
            else:
                cliente.correo = 'Sin correo'                

            # se guarda (actualiza) el cliente
            cliente.save()

            # hacemos el mensaje de exito
            success = 'Cliente <i>{cliente}</i> editado con éxito'.format(cliente=cliente.nombre)

            # se renderea el perfil del cliente editado, junto al mensaje de exito
            return render(request, 'clientes_ver.html', {'c': cliente, 'messages': success})

    # si el request es de tipo GET...            
    else:
        # creamos el formulario de editar y lo llenamos 
        # con la informacion del cliente que se quiere editar
        form = ClienteForm(initial=cliente.__dict__)

        # rendereamos dicho formulario con la tempalte `clientes_editar.html`
        return render(request, 'clientes_editar.html', {'form': form, 'c': cliente})

def clientes_borrar(request, id):
    '''Funcion para borrar un cliente a partir de su ID.'''

    # esta funcion solo es accesible a traves de un metodo POST
    if request.method == 'POST':

        # se obtiene el cliente 
        cliente = Cliente.objects.get(id=id)

        # borramos el cliente
        cliente.delete()

        # finalmente redirigimos a la lista de todos los clientes
        return redirect(clientes_lista)
    
    # si se quiere acceder a traves de GET, se redirigira al perfil del cliente
    # esto se hace como una medida de seguridad
    # (no se debe alterar informacion a traves de requests tipo GET)
    else:
        return redirect(clientes_ver, id=id)


'''__________________________________________________________________'''
def chofer_ver(request, id):
    chofer = Chofer.objects.get(id=id)
    return render(request, 'chofer_ver.html', {'c': chofer})



def choferes_nuevo(request):
    if request.method == 'POST':
        form = ChoferForm(request.POST)
        if form.is_valid():
            nuevo = Chofer()
            nuevo.nombre = form.cleaned_data['nombre']
            nuevo.telefono = form.cleaned_data['colonia'] 

            if form.cleaned_data['correo']:
                nuevo.correo = form.cleaned_data['correo']
            else:
                nuevo.correo = 'Sin correo'  

            nuevo.save()

            success = '''Chofer <i>{chofer}</i> creado con éxito. <a href="/chofer/nuevo" 
            class="alert-link">¿Crear otro?</a>'''.format(chofer=nuevo.nombre)

            return render(request, 'chofer_ver.html', {'c': nuevo, 'messages': success})
            
    else:
        form = ChoferForm()      
        return render(request, 'chofer_nuevo.html', {'form': form})



def chofer_editar(request, id):
    chofer = Chofer.objects.get(id=id)    
    if request.method == 'POST':
        form = ChoferForm(request.POST)
        if form.is_valid():
            chofer.nombre = form.cleaned_data['nombre']
            chofer.telefono = form.cleaned_data['telefono']
        
            if form.cleaned_data['correo']:
                cliente.correo = form.cleaned_data['correo']
            else:
                cliente.correo = 'Sin correo'                

            cliente.save()

            success = 'Chofer <i>{chofer}</i> editado con éxito'.format(cliente=cliente.nombre)

            return render(request, 'chofer_ver.html', {'c': cliente, 'messages': success})
            
    else:
        form = ChoferForm(initial=chofer.__dict__)
        return render(request, 'clientes_editar.html', {'form': form, 'c': cliente})
