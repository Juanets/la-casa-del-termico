# la-casa-del-termico
Sistema de generación de rutas óptimas para La Casa del Térmico.

## Documentación

#### 1. [Uso de Git](/docs/GIT.md)
#### 2. [Instalación de cosas necesarias para el proyecto](/docs/INSTALL.md)
#### 3. [Correr el proyecto](/docs/RUN.md)

## TO-DO

#### 1. Choferes
* Crear choferes
  * Formulario de creaer chofer en `crud/forms.py`
    * Se pueden basar en la clase `ClienteForm` que está en `crud/forms.py`
  * View de crear chofer en `crud/views.py`
    * Chequen la función `clientes_nuevo()` en `crud/views.py`
  * Template de crear chofer. 
    * Crear en `templates/chofer_nuevo.html` 
    * Basarse en `static templates/chofer_nuevo.html`
  * Poner URL en `crud/urls.py`
    * Que la URL se llame `chofer/nuevo/`
* Editar chofer
  * View para editar a chofer en `crud/views.py`
    * Basarse en la función `clientes_editar()` del archivo `crud/views.py`
  * Template para editar al chofer en `templates/chofer_editar.html`
    * Es igual a `chofer_nuevo.html` pero con otro color y título. Chequen `static templates/clientes_editar.html`
  * Poner URL en `crud/urls.py`
    * Que la URL sea `chofer/editar/<int:id>/`
* Ver choferes existentes
  * Hacer view en `crud/views.py`. 
    * Tiene que jalar a todos los choferes (3-4) desde la base de datos.
    * Renderizar dicha información en la template `chofer_ver.html`
  * Hacer la template en `templates/chofer_ver.html`
    * Basarse en `static templates/chofer_ver.html`
  * Agregar URL
    * Que se llame `choferes/`
#### 2. Mapa de clientes
* Hacer un mapa de Google dinámico que muestre todos los clientes en el mapa.
#### 3. Generación de ruta
* Selección de clientes para la ruta
  * Agregar la URL en `rutas/urls.py`, crear si no existe
    * Que se llame `rutas/nueva/`
  * Hacer la view en `rutas/views.py`
    * Debería de jalar a todos los clientes y mandarlos a la template `rutas_escoger_clientes.html`
  * Hacer la template en `templates/rutas_escoger_clientes.html`
    * Basarse en `static templates/generar_rutas.html`
    * La documentación del campo para buscar está [aquí](https://silviomoreto.github.io/bootstrap-select/examples/#live-search)
  * Ver cómo usar jQuery o algo para que aparezcan más campos de búsqueda al clickear en `Agregar otro`    
  * Investigar cómo usar [django-searchable-select](https://github.com/and3rson/django-searchable-select)
  * Crear URL de ruta generada
    * Que sea `rutas/nueva/<str:clientes>/` en `rutas/urls.py`
  * Tomar los clientes seleccionados y mandarlos a la URL `rutas/nueva/<str:clientes>/` al clickear boton `Generar ruta`
* Llamar a API de Maps
  * Usar los clientes seleccionados, obtener sus coordenadas y llamar a la API a través de la URL
  * La llamada a la API regresa datos de la ruta (tiempo, distancia, etc.) 
    * Guardar dichos datos en base de datos
#### 4. Reportes
