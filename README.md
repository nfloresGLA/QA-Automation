# Curso QA Automation

## Temario:

## 1. Introduccion.

### 1.1 - ¿_Que son las pruebas automatizadas_?
> Son procesos de revision y validacion de un producto
llevadas a cabo por una herramienta especializada
que controla su funcionamiento.

> ¿_Que podemos automatizar_?

Casos de prueba donde:
- Se ejecutan rapidamente.
- Son tediosos o complejos.
- Llevan mucho tiempo.

> ¿_Cuando se requiere esto_?
- Se requiere regresiones.
- Se requiere precision en las pruebas.

> ¿__Que no podemos automatizar__?
- Hay cambios frecuentes.
- Las soluciones no son estables.
- Las pruebas no aportan valor.

* Son utilizadas __principalmente__ para garantizar el correcto funcionamiento de una aplicacion a lo largo del
tiempo __ahorrando__ costos de regresion.
### 1.2 - Casos de uso del Testing automatizado.
> Busca resolver la validacion de procesos __complejos__
y __extensos__ a partir de un trabajo _rapido_ y _eficaz_.
Su importancia radica en la ejecucion de tareas
__repetitivas__ en secciones _estables_ y _fijas_.


> __Casos de uso__.

![image](https://user-images.githubusercontent.com/120741890/214369054-7b43d7bb-d2e4-412d-a1a2-cde8040d6515.png)

* El enfoque en este curso sera de automatizar
solo pruebas de __integracion__.

### 1.3 - Scripting.
> Es un conjunto de instrucciones escritas en codigos
que se encargan de ejecutar diversas funciones en el
interior de un programa o sistema.

> ¿_Cual es su funcion_?
- Combinar componentes.
- Interactuar con el sistema operativo o con el usuario.
- Controlar un determinado programa, aplicacion o sistema.

> ¿_Que tareas podemos automatizar con el scripting_?
- __Generacion de datos__: para la ejecucion de pruebas.
- __Limpieza de datos__: Datos en BD y caches.
- __Testing en datos__: Realizar pruebas a un gran volumen de datos.

---

## 2. __Patrones__.

### 2.1 - Patrones de diseño de pruebas.
> Conjunto de metodos para la definicion de jerarquias
de clases que permiten dar solucion a los problemas
mas comunes que se presentan en el desarrollo
de sistemas informaticos eficientes, flexibles y evolutivos.

"Es un conjunto de buenas practicas que agilizan el 
desarrollo de un sistema".

> ¿__Cuales son sus beneficios__?
- _Reducir_ la __curva de dificultad__ para su adquisicion.
- Generar codigo _entendible_ y _estandarizado_.
- _Reducir_ los __costos__ de mantenimiento.

> __Patrones__ de diseño de pruebas:

![image](https://user-images.githubusercontent.com/120741890/214372227-b2e50be0-cff4-4fa0-88a1-cd85af087145.png)

### 2.2 - PageObject

> __Contexto__:

Proyectos que requieran mas de un caso de prueba
sobre la __misma funcionalidad__.

> __Solucion__:

Crear clase __independiente__ con los localizadores
de objetos.

> __Resultado__:

Al cambiar un elemento web _se actualiza solo en la 
clase de localizadores_ y __no__ en __todas__ las pruebas.

> __Problemas__: 
- Suelen __extenderse__ demasiado las clases.
- __No__ cumple con el principio de unica responsabilidad.

> __Diagrama de clase__.

![image](https://user-images.githubusercontent.com/120741890/214373976-6dd848bc-3aff-4905-b8e9-6c4366e9943c.png)
