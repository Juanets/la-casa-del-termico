## Instalación de cosas necesarias
* [Python](https://www.python.org/downloads/release/python-364/)
* [Git](https://gitforwindows.org/)
* Editor de texto (VS Code, Sublime Text, el que sea)

## Bajar este repositorio a su PC
Abrir una terminal (preferentemente **Git Bash**) y correr:
```
git config --global user.name "Tu nombre de usuario en GitHub"
git config --global user.email "Tu correo"
```
Esto es para que se guarden sus datos de sesión en su PC.  
  
Después correr (les pedirá contraseña, para arreglar ver [aquí](https://github.com/Juanets/la-casa-del-termico/blob/master/docs/GIT.md#c%C3%B3mo-guardar-tus-credenciales-para-que-git-deje-de-pedir-tu-contrase%C3%B1a)):

```
git clone https://github.com/Juanets/la-casa-del-termico.git
```

## Instalar el proyecto localmente
Aquí hay dos formas: utilizando `virtualenv` (entorno virtual del proyecto) o instalar todo directamente en su PC.  
Utilizar entornos virtuales es más seguro y mantiene un mejor orden de librerías de Python en su compu, además de ser el estándar para programar en Python... pero si se les hace muy confuso instalen directamente en su PC.
* Con `virtualenv` (recomendado)
  1. Instalar `virtualenv`
  ```
  pip install virtualenv
  ```
  2. Entrar a la carpeta del proyecto
  ```
  cd la-casa-del-termico
  ```
  3. Crear el `virtualenv` (entorno virtual) en donde se instalarán las librerías del proyecto.  
  Por ejemplo: `virtualenv venv`. Esto creará una carpeta `venv`; ahí se instalaran las librerías (django, api de maps). Esto para tener un orden y no mezclar las librerías sus otros proyectos. O sea, en la carpeta `venv` estará todo lo necesario para **este** proyecto.
  ```
  virtualenv <nombre>
  ```  
  4. Activar el entorno virtual.  
  Veran que les aparece `(venv)` en la terminal. Esto indica que el entorno está activado y los comandos (Python, django) se correrán a través de lo instalado *dentro* de la carpeta `venv`.
  ```
  source venv/Scripts/activate
  ```
  5. Ya activado, pueden instalar las librerías para el proyecto.  
  Dichas librerías están enlistadas en el archivo `requirements.txt`. 
  ```
  pip install -r requirements.txt
  ```
* Instalación directa
  1. Entrar al proyecto
  ```
  cd la-casa-del-termico
  ```
  2. Instalar librerías
  ```
  pip install -r requirements.txt
  ```
* **Ojo**: si utilizaron el entorno virtual, tendrán que activarlo con `source venv/Scripts/activate` como se indica en el paso *iv* **cada vez que inicien la terminal**. Si no, la terminal no encontrará las librerías para el proyecto.
