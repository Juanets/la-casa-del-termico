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
#### 3. ~~Generar la ruta~~
#### 4. Reportes
* ~~Guardar la ruta generada en la base de datos~~
* ~~Generación dinámica de PDFs~~
* Darle formato bonito y mostrar la mayor cantidad de información posible
  * El reporte se hace en HTML y se transforma a PDF. Checar `templates/pdf.html`
    * Basarse en `templates/pdf.html` y modificarlo para mejorar formato/agregar información
  * Investigar cómo guardar el mapa mostrado (`iframe`) como imágen y pegarlo en el PDF
  * Agregar el logo de la empresa
* ~~Hacer vista para mostrar el reporte como HTML en la URL `/reportes/<id>/`~~
* ~~Hacer la vista con el listado de todos los reportes~~
  * ~~Poner en la URL `/reportes/`~~
  * ~~Basarse en `static templates/reportes.html` y `templates/clientes_lista.html` para el HTML~~
  * ~~Basarse en la función `clientes_lista` de `crud/views.py` para el código~~
* ~~Lo mismo de arriba pero para un chofer en específico~~
  * ~~Poner en la URL `/reportes/?chofer=<chofer>/'~~
