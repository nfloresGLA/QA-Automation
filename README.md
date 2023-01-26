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

### 4.2 - Pybot Framework

> ¿_Que es_?

Es un framework construido en python y compuesto
por multiples librerias que permiten automatizar
pruebas sobre diversas plataformas.
Esta basado en el patron Page Object, pero con el avance
de su desarrollo se le incorporo algunas caracteristicas
de otros patrones tales como ScreenPlay y Command.

> ¿_Cuales son sus caracteristicas_?

- La solucion es muy flexible.
- Facil de integrar con otras herramientas.
- Compatible con diferentes metodologias de Testing (Cucumber)
- Preparado para adaptarse a procesos CI/CD
- Integra reportes en sus librerias.
- Es seguro debido a su modo de almacenar credenciales.
- Escalable.
- Facil e intuitivo de aprender.

> ¿_Cuales son sus __principales__ librerias_?

- __Unittest__: _Funciones_ que permiten el _armado_ del __cuerpo__
de las pruebas.

- __Pytest__: _Facilita_ la __ejecucion de las pruebas__ y la generacion de metadatos __resultantes__.

- __Request__: Ejecuta llamados a servicios API REST.

- __Allure__: Complementa el armado de pruebas con metadatos
que luego seran utilizadas para generar reportes.

- __Selenium__: Incorpora WebDrivers para la automatizacion
de Browsers (Chrome, Edge y Firebox)

- __Lackey__: Funciones para la automatizacion de inputs
al sistema. Tambien interpreta imagenes y las compara.

> __Composicion__.

![image](https://user-images.githubusercontent.com/120741890/214395154-cb96c354-b426-423b-a1fe-37ff3dd9419d.png)

### 4.3 - Estructuracion de Pybot
> Esta dada por los CP que son agrupados por funcionalidad
dentro de archivos Python "Test Class".
El framework hace uso del __layout__ de funciones que
ofrece la libreria __Unittest__.

~~~ py
# (nombre de la Clase, de donde hereda)
Class Pruebas(Framework, unittest):
    def setUp(self):
        Actions
    def test_000_descripcion(self):
        self.flujo_principal()
    def test_001_descripcion(self):
        self.flujo.alternativo()
    def flujo_principal(self):
        Steps # Defino el camino principal
    def flujo_alternativo(self):
        Steps # Defino el camino alternativo
    def tearDown(self):
        Actions # Defino el cierre de la ejecucion de la prueba
~~~

> __Estructura__.

#### Representado por __niveles__ de mayor a menor.

📁 1. __Carpeta principal__.

 ➞ Almacena la herramienta Pybot y los proyectos.
___
📁 2. __Drivers__.

 ➞ Carpeta autogenerada luego de la primera ejecucion
de un CP. Controlan los browsers.
___
📁 2. __functions__.

 ➞ Contiene todos los archivos para automatizar
utilizando Python.

📁 3. src.

 ➞ Contiene todos los recursos para la herramienta
de ejecucion.
___

📁 2. __projects__.

 ➞ Almacena todos los archivos de los proyectos.

📁 3. __nombre del proyecto__.

 ➞ Almacena todos los archivos de un proyecto. <br>
El nombre no debera tener espacios.

📁 4. __src__.

 ➞ Almacena todos los archivos de un proyecto.

📁 5. dowloands.

 ➞ Almacena todos los archivos descargados durante la ejecucion.

📁 5. files.

 ➞ Almacena archivos varios. Puede usarse para guardar
evidencia, archivos de config o funciones.

📁 5. images.

 ➞ Almacena imagenes que pueden utilizarse para
automatizacion por imagenes con Sikuli.

📁 5. outpus.

 ➞ Almacena archivos de salida de los scripts.
Puede utilizarse para la generacion de reportes csv u otros.

📁 5. resources.

 ➞ Almacena archivos .xlsx que contienen datos de inputs
necesarios para los casos de prueba automatizados.

📁 5. pages.

 ➞ Almacena archivos .json con los elementos capturados de una aplicacion web.

📁 5. tests.

 ➞ Almacena todos los archivos Python con las pruebas
automaticas.

___

📁 2. __venv__.

 ➞ Contiene un entorno virtual de Python.
Su generacion es opcional. <br>
Pero es necesaria generarla para los procesos y las
actividades del framework.

---

## 5. Localizadores.

### 5.1 - Repositorio de objetos.
> Garantiza la _administracion_, _reutilizacion_ y _fiabilidad_ de los elementos de una IU, al capturarlos como objetos en un repositorio al estilo DOM, _compartible_ entre
proyectos.

> __Introduccion__.

Los objetos deben ser almacenados dentro del archivo con extension .__json__ contenidos en la carpeta de _pages_ del proyecto.

![image](https://user-images.githubusercontent.com/120741890/214415170-2e8caef9-693f-491c-89cf-7a845cb915a4.png)

### 5.2 - Tipos de localizadores.
> Es un __comando__ que le dice a Selenium que _elementos_ de la interfaz 
necesita para operar y la correcta identificacion de estos elementos
__es un requisito previo__ a la creacion de una secuencia de comandos de automatizacion.

> __Tipos__.
- __ID__: Es la mejor opcion siempre que sean unicos e invariantes en el tiempo.
- __Name__: El atributo no tiene que ser unico, por lo que el uso de este
localizador no garantiza que las pruebas se produzcan de la manera deseada.
- __Xpath__: Hace uso de la estructura XML que posee todo documento html 
para asi hacer referencia a los elementos mediante una ruta que puede 
ser __absoluta__ o _relativa_.

Existe el _problema_ que cualquier __introduccion de un nuevo elemento__
 o la __reorganizacion de los existentes__ provoque que las __referencias cambien__, 
 lo que __puede invalidar__ las pruebas grabadas anteriormente.

> Ademas __Selenium__ admite:
- __CSS Selector__: Consiste en identificar los elementos por sus propiedades de css.
- __DOM__ (Document Object Model): Es similar al Xpath, pero
utiliza el DOM de la pagina para hacer referencia a los elementos

> __Localizar__.
A traves del uso de los localizadores <Locators> podemos
identificar con que elemento GUI <web element> queremos
trabajar agregandole el valor <target> de referencia
que el localizador tenga asociado.

### 5.3 - Localizador especial __Xpath__.
> Es un lenguaje que permite construir expresiones
que recorren y procesan un documento XML o el DOM de una
aplicacion web. Es parecido a una expresion regular para
seleccionar partes de un texto sin atributos. <br>
Permite buscar y seleccionar teniendo en cuenta
la jerarquia dentro del DOM.

![image](https://user-images.githubusercontent.com/120741890/214423075-20798292-b2e0-4854-bdd2-b5d238824c67.png)

---

## Instalacion de Pybot - __Requisitos previos__.

~~~ ts
> Tener instalado PyCharm.
// Version de esta guia: PyCharm 2022.3.1 (Community Edition)
> Tener instalado Python
// Version de esta guia: Python 3.9.9
> Descargar el archivo CursoQA y agregarlo en C:\
// Nos quedaria el path de ruta: "C:\CursoQA"
> Tener bien configuradas las variables de entorno
// Ver detalle mas abajo.
~~~

* __Variables de entorno__ .

###  *_Despues de instalar Python <u>correctamente_</u>.

1. Ingresar en:

![image](https://user-images.githubusercontent.com/120741890/214583124-16506e07-cb8b-42b4-b333-b9e3f63fad25.png)

2. Doble click sobre "__Path__"

![image](https://user-images.githubusercontent.com/120741890/214583684-4445f190-54d4-4f5b-8c16-3a59bea9671f.png)

3. Verificar de tener dentro del __path__ estos valores.

* En caso de no tener alguno agregarlos.

![image](https://user-images.githubusercontent.com/120741890/214864844-c5803bd9-eaaa-45a6-ba7f-94ae2ae6c3d9.png)

---

### Instalacion de Pybot - Pasos.

1. __Dentro__ de la 📁 carpeta: __functions__ en una terminal _*_

~~~ py
 pip install -r "requirements for win.txt" 
~~~

~~~ py
# * Una manera facil de acceder a la consola:
# Click derecho: mas opciones / abrir en terminal
~~~

* Tarda alrededor de 2/3 minutos la instalacion de los paquetes


2. Entrar en __PyCharm__
### Vista del __primer inicio__

![image](https://user-images.githubusercontent.com/120741890/214571409-7f43f438-1270-49e1-8439-2f3cbd376e9f.png)

* Click en _Open_ para elegir la carpeta del proyecto

![image](https://user-images.githubusercontent.com/120741890/214572914-7949b93c-6ebb-4d2d-9269-977268adcdef.png)

* _¡Importante_! para facilitar la agregacion del curso
agregar la carpeta de CursoQA al directorio de C: como
se muestra en pantalla.

* Seleccionar CursoQA (tiene que quedar como directory)

![image](https://user-images.githubusercontent.com/120741890/214573249-43ca0554-6411-422d-8105-9e4df4bc9e8a.png)

* Click en "Confiar en el directorio" -> __Trust Project__

* Esto nos cargara el projecto del framework
(__Puede demorar un poco__)

![image](https://user-images.githubusercontent.com/120741890/214580052-67978dbf-54b4-44b1-9c65-f802c378f577.png)

* Asegurarse que la 📁 carpeta sea CursoQA y no Functions
(Subrayado en __amarillo__)

* __Asegurarse__ que los _niveles_ sean:
- 1: __CursoQA__
- 2: __Functions__
- 3: __.idea / src__

* Los niveles corresponden al subrayado en __rojo__.


<p>
 A partir  de este momento se puede seguir en el video:
    <a 
        href="https://www.youtube.com/watch?v=zn8deBB8DXY&list=PLBOWOYkuapWjOB8ZNjZ9hlz4k1CK3bEho&index=20" 
        target="_blank">
        QA Automation 6x3
    </a>
</p>

---