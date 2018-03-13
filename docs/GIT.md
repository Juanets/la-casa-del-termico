## ¿Qué es Git y cómo lo uso?
Abraham explica muy bien qué es Git en [estas slides](https://docs.google.com/presentation/d/1SsnPKpCuVecgbrOxxF0UK9zToLkh1CY6Q0zwtzdllNU/edit#slide=id.g31e99f0598_0_499).
Parece mucho (67 diapositivas) pero realmente es poco, además de ser **demasiado** útil. También te explica los comandos básicos de la terminal y otras cositas.  
  
También pueden echarse videos en YouTube o tutoriales interactivos como [este](https://try.github.io) o [este](http://gitreal.codeschool.com/) (aquí aprendí yo, recomendado).

## Uso de Git en el proyecto

Nosotros sólo usaremos 5 comandos básicos de Git: `checkout`, `add`, `commit`, `push` y `pull`. 

### 1. [Checkout](#)
La rama principal es la `master`, pero hay que tener cuidado al trabajar en esta rama ya que es donde está el proyecto principal y no queremos que sucedan accidentes. Por eso, cada quien trabajará en su rama y una vez que hagan algo que deseen integrar a la rama principal, [harán solicitudes a través de pull requests](#).  
  
`git checkout` se usa para cambiar a una rama existente.
```
git checkout juanito
```
Si la rama no existe, el comando dará error. Se debe utilizar el argumento `-b` para crear la rama. 
```
git checkout -b alan
```
Esto, además de crear la rama `alan`, te cambia a esa rama (si se fijan, en la terminal ya no aparece *(master)*, aparecera el nombre de la rama a la que te hayas cambiado).
### 2. [Add](#)
Imaginen que son empaquetadores de Amazon, y cada vez que llega un pedido, deben echar los articulos del pedido a una caja y prepararlos para que alguien lo empaquete.  
  
`git add` basicamente es eso: agrega archivos a una "caja" para prepararlos, despues se *commitean* y al final se *pushean* a la rama principal, para que estén disponibles en el repositorio (aquí, en GitHub).  
  
Cada vez que hagan algo importante o un **avance significativo** en su parte del proyecto hagan esto:
```
git add <nombre del archivo>
```
Si quieren hacer `add` a toda la carpeta, simplemente:
```
git add .
```
Ejemplo, agregando tres archivos:
```
gid add templates/ruta_generada.html templates/ver_clientes.html static/css/estilos.css
```
Listo, los cambios a dichos archivos están guardados y preparados para que sean *commiteados*.
### 3. [Commit](#)
Siguiendo la analogía de Amazon... ahora que los articulos del pedido están seleccionados, ahora viene el empaquetado. Los guardas en un sobre, le pones la etiqueta con la dirección, la información del pedido y cliente, etc.  
  
`git commit` crea un registro, con información de quién hizo los cambios, qué cambios, qué rama, qué archivos, fecha. Es como poner "en papel" los cambios/avances que hiciste en el proyecto.  
```
git commit -m 'Se actualizaron los estilos CSS de dos vistas'
```
Esto "empaqueta" los cambios que hicimos con `git add` en el ejemplo anterior **en un solo commit**, y se le pone como mensaje `Se actualizaron los estilos CSS de dos vistas`. El argumento `-m` significa `message` y es obligatorio ponerlo en cada commit.  
  
Si quieren ver un ejempo/representación visual de commits, vean los commits que se han hecho hasta ahora [en este mismo proyecto](https://github.com/Juanets/la-casa-del-termico/commits/master).  
  
Pueden dar click en uno y ver qué cambios se hicieron. Por ejemplo [este](https://github.com/Juanets/la-casa-del-termico/commit/8e05f4b174fd59d759bdd166147aa8bf9aebf16a). Del lado izquierdo, en rojo, es como era antes. Del lado derecho aparecen los cambios en color verde.
### 4. [Push](#)
Una vez listo el paquete (articulos pedidos, informacion de envio y cliente, etc) se envía al destino.  

`git push` hace eso: se envían los commits (paquete de archivos y sus cambios) al repositorio remoto.  
Recuerden que cada quien trabajará en su rama, por lo tanto **el push se deberá hacer a su rama**.
```
git push origin alan
```
El `origin` es el servidor de origen del repo; siempre será igual. Después ponen el nombre de la rama a la que van a *pushear*.
Si llegaran hacer push a `master` simplemente sería:
```
git push origin master
```
Y así es como envían su trabajo al repositorio para que todos trabajemos en el mismo proyecto con los mismos avances.  

---

En ocasiones, Git dirá algo como "El repositorio remoto contiene cosas que tú no tienes localmente". Significa que tienen que tener la versión más reciente del repo para poder subir cambios. Esto es debido a que, si ustedes tienen archivos pasados con cambios viejos, y quieren *pushearlos* al repo, entonces se borraría la información más nueva del repositorio y se perdería todo.  
  
Para bajar la versión más reciente del repositorio se tiene que hacer `git pull`.  

### 5. [Pull](#)
Este es fácil. Simplemente ponen el remoto y la rama.
```
git pull origin alan
```
Así se bajan los cambios que estén en el repositorio en la rama `alan`.  
  
Si quieren hacer pull desde la rama principal, entonces:
```
git pull origin master
```
Puede ser que surgan *conflictos de merge* (es muy raro, pero pasa). La terminal les dirá que en tal linea surgió un conflico y que lo arregles manualmente. Es algo confuso, pero si les pasa me pueden pedir ayuda. Si quieren arreglar dichos conflictos [aquí se explica cómo](https://github.com/oslugr/curso-git/blob/master/texto/solucion_problemas.md#resolviendo-conflictos).

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
