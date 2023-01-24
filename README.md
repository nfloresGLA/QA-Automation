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


### 2.3 - ScreenPlay

> __Contexto__:

Proyecto de pruebas automatizadas que tengan
mas de un caso de prueba sobre la misma
funcionalidad y de __gran tamaño__.

> __Solucion__:

Adicional a la clase contenedora de los localizadores
de objetos, se crean clases _encargadas_ de realizar
__acciones__ y otra con tareas.

> __Resultado__:

_Se reduce tamaño de clases_.
Se estructura el proyecto de manera
mas __organizada__.

> __Problemas__:

- Suele resultado __complejo__ el entendimiento para su implementacion

> __Diagrama de clase__.

![image](https://user-images.githubusercontent.com/120741890/214375999-ebab841b-1a4d-4531-acf0-43930b30f40a.png)

### 2.4 Command.
> Se podria definir como complemento, ya que puede
ser implementado en conjunto de otros patrones
permitiendo escalar el tamaño de las pruebas segun
lo requiera el proyecto.

> __Contexto__:

Proyectos de pruebas automatizadas que ya esten
usando otros patrones o cualquiera que tenga mas de
un caso de prueba sobre la misma funcionalidad.

> __Solucion__:

Crear una clase que contenga un comando con el paso
a paso de la prueba, adicional a una clase con localizadores
de objetos. Cada clase tendria responsabilidades
independientes.

> __Resultado__:

Al cambiar un elemento web se actualiza solo en la clase
de localizadores y no en todas las pruebas.
Las clases _command_ son representativas en funcion
a la funcionalidad.


> __Problemas__:

Dificultad en el mantenimiento ya que este patron es
complementario a otros patrones.
Se requiere reglas claras de uso.

> __Diagrama de clase__.

![image](https://user-images.githubusercontent.com/120741890/214379249-5f02ba33-bbec-4cb2-a946-b705c983e8c9.png)

---

## 3. __Python__.

### 3.1 - Conociendo Python.

> Es un lenguaje de programacion __interpretado__ de tipado
_dinamico_, cuya filosofia plantea una sintaxis que "_favorezca_" a un codigo __legible__. <br>
Es un lenguaje __multiproposito__, __multiparadigma__ y se encuentra disponible en varias plataformas.

### 3.2 - Caracteristicas de Python.

> __Caracteristicas__:

- __Interpretado__: Se ejecuta sin necesidad de ser 
procesado por un compilador y se detectan los errores
en tiempo de ejecucion.

- __Multiparadigma__: Soporta programacion funcional,
imperativa y programacion orientada a objetos.

- __Multiplataforma__: Disponible para windows, Linux o Mac.

- __Tipado dinamico__: Las variables se comprueban en
tiempo de ejecucion.

- __Gratuito__: No se requieren licencias para utilizarlo.

### 3.3 - Motivos para elegirlo.

> __Motivos__

- Amigable: Es facil de aprender y mantener.

- Comunidad: Tiene soporte provisto por la comunidad.

- Competente: Posee gran cantidad de librerias multiproposito.

- Libre: Es de codigo abierto.

## 4. Frameworks.
### 4.1 ¿Que es un framework?
> Podria definirse como un _entorno_ de trabajo
predispuesto, que posee ciertas herramientas, _criterios_ y
caracteristicas que resultan utiles para __agilizar__ el
desarrollo de un proyecto.

Puede reducir drasticamente la aparicion de errores al
desarrollar nuevos componentes.

Los framework se caracterizan por seguir un __conjunto
de practicas y criterios de forma estandarizadas__.

Por lo general son construidos en base a la experiencia
obtenida de trabajos realizados anteriormente.