## ¿Qué es Git y cómo lo uso?
Abraham explica muy bien qué es Git en [estas slides](https://docs.google.com/presentation/d/1SsnPKpCuVecgbrOxxF0UK9zToLkh1CY6Q0zwtzdllNU/edit#slide=id.g31e99f0598_0_499).
Parece mucho (67 diapositivas) pero realmente es poco, además de ser **demasiado** útil. También te explica los comandos básicos de la terminal y otras cositas.  
  
También pueden echarse videos en YouTube o tutoriales interactivos como [este](https://try.github.io) o [este](http://gitreal.codeschool.com/) (aquí aprendí yo, recomendado).

## Uso de Git en el proyecto

Nosotros sólo usaremos 5 comandos básicos de Git: `checkout`, `add`, `commit`, `push` y `pull`. 

### 1. [Checkout](#)

### 2. [Add](#)

### 3. [Commit](#)

### 4. [Push](#)

### 5. [Pull](#)

## Comandos extra

### 1. [Status](#)

### 2. [Init](#)

### 3. [Clone](#)

## Cómo guardar tus credenciales para que Git deje de pedir tu contraseña
Como el proyecto está privado, cada acción que hagan (clone, pull, push) requerirá de su contraseña. 
Sus credenciales (usuario y contraseña) se pueden guardar localmente para que Git ya no enfade.
```
git config credential.helper store
```
Esto guarda un archivo oculto en algún lugar de su PC y serán las que Git use para todo lo que hagan.
<sup>[[source]](https://stackoverflow.com/questions/7773181/git-keeps-prompting-me-for-password/11428767#11428767)</sup>
