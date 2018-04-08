## Correr el proyecto
Después de haber clonado el proyecto a su PC y preparar todo ([sección 2](/docs/INSTALL.md/)), ya pueden correr el proyecto localmente.  
  
Estando en la carpeta raíz del proyecto, corran 
```
python manage.py createsuperuser
```  
Esto es para crear un usuario administrador con todos los derechos. No es 100% necesario pero es posible que lo ocupen más adelante.

Para correr el servidor, se utiliza el comando `runserver`
```
python manage.py runserver
```
Esto abrirá un puerto en el localhost (127.0.0.1:8000). Entren ahí y listo.
