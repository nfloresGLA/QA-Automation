# -*- coding: utf-8 -*-
import os, sys
import gevent
import http.client
import requests
basedir = os.path.abspath(os.path.join(__file__, "../../../../.."))
sys.path.append(basedir) #Resuelve el problema de la ejecucion por consola
from locust import HttpUser, task, between, constant, LoadTestShape, TaskSet, constant_pacing
from locust.env import Environment
from locust.stats import stats_printer, stats_history
from locust.log import setup_logging
from functions.Parameters import Parameters
from functions.Functions import Functions as Funciones
import time


setup_logging("INFO", None)

class Functions(Parameters):
    server = Parameters.server
    port = Parameters.port
    max_threads = Parameters.max_threads
    rate = Parameters.rate
    duration = Parameters.duration
    wait_time = Parameters.wait_time

    def set_proyect(self, proyect_name=None):

        '''

        Description:
            Implementacion del metodo Function.set_proyect (Configura las rutas de los recursos)

        Args:
            proyect_name: nombre de la carpeta del proyecto desde donde se ejecuta el script.

        '''

        Funciones.set_proyect(self, proyect_name)

    def get_row_excel(self):

        '''

        Description:
            Implementación del metodo Function.get_FilaExcel (Obtiene el numero de row del resource).

        Returns:
            Devuelve el numero de row actual.

        '''

        return Parameters.row

    def leer_celda(self, celda="A2", file_name=None, sheet=None):

        '''

        Description:
             Implementacion del metodo Function.Leer_celda (Obtiene el value de una cell del resource).

        Args:
            celda: Celda del resource a leer
            file_name: Nombre del resource correspondiente al caso.
            sheet: Hoja del resource a consultar.

        Returns:
            Devuelve el value alojado en la cell del resource.

        '''

        return Funciones.read_cell(self, celda, file_name, sheet)

    def set_configuration(self,server=server, port=port, max_threads=max_threads, rate=rate,
                          duration=duration, wait_time=wait_time):

        '''

        Description: Configura las condiciones de stress y carga de la prueba.

        Args:
            server: Server de la UI de Locust.
            port: Port de la UI de Locust.
            max_threads: Cantidad maxima de usuarios.
            rate: Rate de spawn de los usuarios.
            duration: Duracion de la prueba.
            wait_time: Tiempo de espera entre el spawn de usuarios.

        Returns:

        '''

        Functions.server = server
        Functions.port = port
        Functions.max_threads = max_threads
        Functions.rate = rate
        Functions.duration = duration
        Functions.wait_time = wait_time

    def get_configuration(self):

        '''

        Description:
            Obtiene la configuracion de la prueba y la imprime en el log.

        Returns:
            Devuelve una tupla con los datos de la confuiguracion...
            Server de la UI de Locust
            Port de la UI de Locust
            Cantidad maxima de usuarios.
            Rate de spawn de los usuarios.
            Duracion de la prueba.
            Tiempo de espera entre el spawn de usuarios.

        '''

        print(f"El server locust esta configurado en la ip: {Functions.server}.")
        print(f"El puerto locust esta configurado en el puerto: {Functions.port}.")
        print(f"La cantidad de hilos esta configurada en: {Functions.max_threads}.")
        print(f"El coeficiente incremental es de: {Functions.rate}.")
        print(f"La duracion de la prueba esta configurada en: {Functions.duration} segundos.")
        print(f"El tiempo de espera entre ciclos es de en: {Functions.wait_time} segundos.")
        return (Functions.server, Functions.port, Functions.max_threads,
                Functions.rate, Functions.duration, Functions.wait_time )

    def run_test(self, User):

        '''

        Description:
            Levanta la UI de Locust en el servior, ejecuta la clase User y baja el servidor una ves finalizado.

        Args:
            User: Clase de usuario HttpUser con la configuracion de la prueba.

        '''
        Functions.server
        Functions.port
        Functions.max_threads
        Functions.rate
        Functions.duration
        
        # setup environment and Runner
        env = Environment(user_classes=[User])
        env.create_local_runner()

        # start a WebUI instance0
        env.create_web_ui(Functions.server, Functions.port)

        # start a greenlet that periodically outputs the current stats
        gevent.spawn(stats_printer(env.stats))

        # start a greenlet that save current stats to history
        gevent.spawn(stats_history, env.runner)

        # start the tests
        env.runner.start(Functions.max_threads, spawn_rate=Functions.rate)

        # in 60 seconds stop the runner
        gevent.spawn_later(Functions.duration, lambda: env.runner.quit())

        # wait for the greenlets
        env.runner.greenlet.join()
        self.save_report_html()

        # stop the web server for good measures
        env.web_ui.stop()


    def execution_load_test_simple(self, dominio: str, urn: str, method: str, headers: str = None, payload: str = None):

        """

        Description:
            Ejecuta un tests de carga sobre un servicio de la aplicacion

        Args:
            dominio: url base por ej https://httpbin.org/
            urn: servicio al que se le ejecutara el tests de carga por ej /ip o /home.html
            method: metodo(GET, POST, DELETE)
            headers: cabezera de la peticion por ej { "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0"}
            payload: datos adicionales que requiere la peticion ej { "numeroEnvio":"G00000354664010" }

        return: lista de tuplas que en formato (tarea x, status_code, response.text)

        """

        if Functions.max_threads <= Functions.rate:
            Functions.set_configuration(self, max_threads=Functions.max_threads, rate=int(0.10*Functions.max_threads),
                                        duration=Functions.duration, wait_time=Functions.wait_time)

        results = []
        class User(HttpUser):
            wait_time = constant(Functions.wait_time)
            wait_time = between(1, 2)
            host = dominio

            @task
            def tarea_001(self):
                response = Functions.send_service(self,method, urn, headers, payload)
                results.append(("Tarea 1:", response.status_code, response.text))

        Functions.run_test(self, User)
        return results

    def execution_load_test_doble(self, dominio : str, urn: list, method: list, headers: list = None,
                                  payload: list = None, priority: list = None):

        """

        Description:
            Ejecuta un tests de carga sobre un servicio de la aplicacion

        Args:
            dominio: url base por ej https://httpbin.org/
            urn: Lista con los servicios que se le ejecutaran en el tests de carga por ej /ip o /home.html
            method: Lista con metodos(GET, POST, DELETE)
            headers: Lista con las cabezeras de las peticiones por ej { "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0"}
            payload: Lista con datos adicionales que requieren las peticiones ej { "numeroEnvio":"G00000354664010" }
            priority: Lista con las prioridades de las tareas.

        return: lista de tuplas que en formato (tarea x, status_code, response.text)

        """

        if Functions.max_threads <= Functions.rate:
            Functions.set_configuration(self, max_threads=Functions.max_threads, rate=int(0.10*Functions.max_threads),
                                        duration=Functions.duration, wait_time=Functions.wait_time)
        else:
            Functions.set_configuration(self, max_threads=Functions.max_threads, rate=Functions.rate,
                                        duration=Functions.duration, wait_time=Functions.wait_time)

        results = []
        class User(HttpUser):
            wait_time = constant(Functions.wait_time)
            host = dominio
            @task(priority[0])
            def tarea_001(self):
                self.wait()
                response = self.client.request(method[0], urn[0], headers=headers[0], data=payload[0])
                results.append(("Tarea 1:", response.status_code, response.text))

            @task(priority[1])
            def tarea_002(self):
                self.wait()
                response = self.client.request(method[1], urn[1], headers=headers[1], data=payload[1])
                results.append(("Tarea 2:", response.status_code, response.text))

            def on_start(self):
                fecha = time.strftime("%d%m%H%M%S")
                print(fecha)

        Functions.run_test(self, User)
        return results

    def execution_stress_test_simple(self, dominio: str, urn: str, method: str, headers: str = None,
                                     payload: str = None):
        '''

        Description:
            Prepara un tests de stres simple de un solo recurso.

        Args:
            dominio: Dominio de la aplicación a estrezar.
            method: Metodo de la peticion. Ejem "GET", "POST", "DELETE"
            urn: Localizacion del recurso a estrezar. Ejm.. ip/tests
            headers (Optional): Headers de la petición.
            payload (Optional): Payload o Data de la peticion.

        Returns:
            Devuelve los response de las peticiones realizadas.

        '''

        if Functions.max_threads != Functions.rate:
            Functions.set_configuration(self, max_threads=Functions.max_threads, rate=Functions.max_threads,
                                        duration=Functions.duration, wait_time=Functions.wait_time)

        results = []
        class User(HttpUser):
            wait_time = constant(Functions.wait_time)
            wait_time = between(1,2)
            host = dominio

            @task
            def tarea_001(self):
                response = Functions.send_service(self,method, urn, headers, payload)
                results.append(("Tarea 1:", response.status_code, response.text))

        Functions.run_test(self, User)
        return results

    def get_user(self):

        '''

        Description:
            Obtiene una clase "User" hija de la clase HttpUser que se utiliza como template para la ejecucion
            de las pruebas.

        Returns:
            Devuelve una clase HttpUser abstracta.

        '''

        class User(HttpUser):
            #wait_time = constant(functions.wait_time)
            wait_time = constant_pacing(Functions.wait_time)
            host = ''
            priority=[1]
            @task (priority[0])
            def tarea_001(self):
                pass
        return User

    def send_service(self, method, urn, headers=None, payload=None):

        '''

        Description:
            Se utiliza para hacer el lanzamiento de los servicios a traves de la libreria Locust.client().

        Args:
            method: Metodo de la peticion. Ejem "GET", "POST", "DELETE"
            urn: Localizacion del recurso a estrezar. Ejm.. ip/tests
            headers (Optional): Headers de la petición.
            payload (Optional): Payload o Data de la peticion.

        Returns:
            Devuelve el response de la peticion.

        '''

        response = self.client.request(method, urn, headers=headers, data=payload)
        return response

    def execution_user_custom(self, user_class: object):

        '''

        Description:
            Prepara el tests de stress utilizando el usuario personalizado.

        Args:
            user_class: Recibe una clase con todos sus metodos personalizados y configurados acorde a la necesidad.

        Returns:
            Una lista con los resultados si esta fuera configurada en la clase User personalizada.

        '''

        self.results = []
        Functions.run_test(self, user_class)
        if self.results == []:
            print("La variable 'self.results' no fue configurada")
        return self.results

    def save_report_html(self):
        '''

        Description:
            Se utiliza para guardar el reporte resultante de la ejecución.

        '''

        url = f"http://{Functions.server}:{Functions.port}/stats/report"
        response = requests.request("GET", url)
        f = open("reporte.html", "w", encoding='utf8')
        f.write(response.text)
        f.close()

    def set_timeout_base_sql_server(self, time_seconds):

        '''

            Description:
               Configura el value de timeout (segundos) configurado para las conexiones a bases sqlServer.

        Args:
            time_seconds:
                Valor (int) que representa una cantidad en segundos.

        '''
        Funciones.set_timeout_base_sql_server(self, time_seconds)

    def get_timeout_base_sql_server(self):

        '''

            Description:
                Devuelve el value de timeout configurado para la conexion a bases sqlServer.

            Return:
                Devuelve el value de timeout (segundos) configurado para la conexion a bases sqlServer.

        '''

        time = Funciones.get_timeout_base_sql_server()
        return time

    def execute_sp_base_sqlserver(self,server, base, usuario, password, consulta, parametros: tuple):

        """

        Description:
            Realiza conexión y consulta a base de datos con la libreria pyodbc. El metodo incluye el cierre la
        desconexion.

        Args:
            server (str): Servidor ip
            base (str): Nombre de la base
            usuario (str): usuario
            password (str): Contraseña
            consulta (str): consulta Query
            parametros (tuple): tupla con parametros para el sp.

        Returns:

            <class 'pyodbc.Row'>: Retorna un class 'pyodbc.Row' si la consulta y la conexión es exitosa. De lo
             contrario imprime por consola "Se produjo un error en la base de datos."

        """

        return Funciones.execute_sp_base_sqlserver(self,server, base, usuario, password, consulta, parametros)