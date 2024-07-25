# radioCenter

* Autor: Ruslan Dolovaniuk (Ucrania)
* PayPal: ruslan.dolovaniuk84@gmail.com

este complemento te permite escuchar estaciones de radio en línea y guardar  el flujo de audio en un archivo.
Grabar una estación de radio no interfiere con escuchar otra estación de radio.

¡Advertencias!
Controlar estaciones de radio de las colecciones es un proceso bastante largo y que requiere muchos recursos.
Se recomienda realizarlo por partes, cerrando periódicamente la ventana y volver a ejecutarlo más tarde.
Después de reabrir la ventana de Colecciones, las pruebas continuarán hasta que se hayan verificado todas las estaciones de radio.
Además, el estado de salud de los enlaces cambia a menudo, por lo que se recomienda verificar el estado del enlace en el momento antes de agregarlo a la lista general.


## Lista de atajos de teclado:
* NVDA+ALT+P: reproducir/pausar la radio;
* NVDA+ALT+P doble clic: desactivar la radio;
* NVDA+ALT+M: silenciar/desilenciar el sonido;
* NVDA+ALT+Flecha arriba: subir el volumen;
* NVDA+ALT+Flecha abajo: bajar el volumen;
* NVDA+ALT+Flecha derecha: siguiente estación;
* NVDA+ALT+Flecha izquierda: estación anterior;
* NVDA+ALT+O: obtener información de la estación;
* NVDA+ALT+R: abrir ventana de Control Radio Center;
* ESCAPE: cerrar las ventanas de Control Radio Center y de Colecciones de Radio;
* CTRL+C: copiar el enlace de la estación de radio al portapapeles;

Al ordenar manualmente en la lista de estaciones:
* ALT+Flecha arriba: mueve la estación a una posición más alta;
* ALT+Flecha abajo: mueve la estación a una posición más baja;

En las listas de colecciones:
* ALT+Flecha arriba o ALT+Flecha derecha: cambiar al siguiente enlace (si la estación de radio tiene varios enlaces al flujo de audio);
* ALT+Flecha abajo o ALT+Flecha izquierda: cambiar al enlace anterior (si la estación de radio tiene varios enlaces al flujo de audio);
* CTRL+C: copiar el enlace de la estación de radio al portapapeles;

## Orden de estaciones:
* sin ordenar;
* por nombre ascendente (de la A a la Z);
* por nombre descendente (de Z a A);
* por prioridad y por nombre ascendente (de la A a la Z);
* por prioridad y nombre descendente (de Z a A);
* manualmente;

## Lista de cambios:
### Versión 3.2.0
* soporte agregado para enlaces .pls;
* agregó un nombre a la información de la transmisión de audio al guardar el archivo grabado;
* Se agregó manejo de errores cuando no se puede iniciar la grabación;

### Versión 3.0.0
* se creó un mecanismo de colección para seleccionar estaciones de radio de catálogos;
* se agregaron 3 colecciones con estaciones de radio;
* se creó un mecanismo para verificar automáticamente la funcionalidad de cada estación de radio en las colecciones;
* se agregó una verificación manual de la funcionalidad de la estación de radio;
* se agregó reproducción de la estación de radio directamente en la lista de colecciones;
* se agregó guardar estaciones de radio de la colección a la lista general;
* filtrado agregado en colecciones por estado;
* filtrado agregado en colecciones por texto en el título;
* filtrado agregado en colecciones por texto en información adicional;
* agregado cerrar cuadros de diálogo pulsando ESCAPE;
* se agregó copiar el enlace de la estación de radio al portapapeles en la lista principal y en las listas de colección;
* conmutación de estaciones mejoradas mediante teclas de acceso rápido, ya que anteriormente no siempre cambiaba;

### Versión 2.1.0
* Se agregó verificación y corrección si se encuentran errores en la indexación de estaciones;
* localización en español agregada (Rémy Ruiz);
* localización francesa agregada (Rémy Ruiz);

### Versión 2.0.0
* se agregó la capacidad de guardar un flujo de audio en un archivo;

### Versión 1.5.3
* localización checa agregada (Jiri Holz);

### Versión 1.5.1
* se agregó una verificación de funcionalidad del enlace antes de agregar una nueva estación de radio;
* se agregó una verificación de la funcionalidad del enlace antes de cambiar el enlace de la estación de radio;
* se corrigieron una serie de errores operativos menores;

### Versión 1.4.2
* ordenación manual agregada de estaciones;
* combinación de teclas agregada para el modo silenciar el sonido;

### Versión 1.2.5
* parámetros añadidos al panel de opciones de NVDA;
* se agregó la capacidad de editar una estación de radio existente;
* se agregaron más opciones para ordenar estaciones de radio;
* se cambió la función de silenciar el sonido;
* se solucionó el problema con la apertura de múltiples ventanas de control;

### Versión 1.1.1
* localización turca agregada (Umut Korkmaz);

### Versión 1.1.0
* se agregó GUI al Control Radio Center;;

### Versión 1.0.0
* creación de una radio en línea en el reproductor VLC básico;
