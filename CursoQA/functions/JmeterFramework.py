# -*- coding: utf-8 -*-
import allure

import functions.SeleniumFramework
from functions.Parameters import Parameters
from functions.Functions import Functions as FunctionsGeneric
import os
import unittest
from datetime import datetime
import shutil
import json

class Functions(FunctionsGeneric, Parameters):

    def set_project(self, project_name=None):

        """

            Description:
                Setea variables de ambiente y rutas del proyecto.

            Args:
                project_name (str): Nombre del proyecto

            Returns:
                Imprime por consola la siguiente configuración:
                    -Ambiente.
                    -Ruta de Resource.
                    -Ruta de Evidencias.
                    -Ruta de los Json.
                    -Ruta de las Imagenes de los json (reconocimiento por imágenes).
                    -Ruta de los Bass.

                Si hubo un error en la configuración, imprime por consola
                "No se pudieron detectar los datos de la ejecución".

        """

        FunctionsGeneric.set_proyect(self, project_name)

    @staticmethod
    def set_path_jmeter_executor(path):

        """

            Description:
                Setea nuevo path en caso de no usar el asignado por defecto.

            Args:
                 path: Ubicación donde se encuentra JMeter.

        """

        Parameters.path_jmeter = path
        print(f"El path del ejecutor Jmeter se encuentra configurado en la ruta '{Parameters.path_jmeter}'.")

    @staticmethod
    def set_config_thread_group(url_jmeter, users_jmeter, rampup_jmeter, duration_jmeter, throughput_jmeter, status_code_expected,
                                parameter_id=None, expected_value=None):

        """

            Description:
                Setea variables que van a ser cargadas al iniciar JMeter

            Args:
                url_jmeter: url que va ser utilizado en el .jmx
                users_jmeter: Cantidad de usuarios virtuales.
                rampup_jmeter: Tiempo en que se van a subir los usuarios virtuales.
                duration_jmeter: Duración de la prueba.
                throughput_jmeter: Controla la cantidad de reuquest enviado por minuto
                status_code_expected: Setea el status code en la  prueba jmx a ejecutar.
                parameter_id: Envia id en caso de que el servicio lo requiere.
                expected_value: Envia valor que se debe esperar en el response.

        """

        Parameters.url_jmeter = url_jmeter
        Parameters.users_jmeter = users_jmeter
        Parameters.rampup_jmeter = rampup_jmeter
        Parameters.throughput_jmeter = throughput_jmeter
        Parameters.status_code_expected = status_code_expected
        Parameters.duration_jmeter = int(duration_jmeter) * 60 #Para pasar la duracion minutos
        Parameters.expected_value = expected_value
        Parameters.parameter_id = parameter_id

    def execute_jmx(self, mode_headless=True):

        """

            Description:
                Levanta JMeter pasando la ubicación del jmeter.bat.

            Args:
                mode_headless: Indicamos con true o false para que inicie JMeter con/sin interfaz gráfica.

        """

        #folder_dashboard = Parameters.path_dashboard

        # limpia la carpeta dashboard_jmeter
        #Functions.clean_dashboard_folder(folder_dashboard)

        escenario_jmx = Functions.get_path_escenario_jmx(self)  # Obtiene la ruta en donde se encuentra el .jmx a utilizar
        result_jtl = Functions.create_and_get_path_report(self) # Crea y obtiene la ruta donde se encuentra el .jtl con el
                                                                # output de la prueba.

        if Parameters.environment == "Windows":
            if mode_headless or Parameters.enviroment_confguration == "Server":
                os.system(f"call {Parameters.path_jmeter} -n -t {escenario_jmx} -l {result_jtl} " #-e -o {folder_dashboard}
                          f"-J URL={Parameters.url_jmeter} "
                          f"-J USER={Parameters.users_jmeter} "
                          f"-J RAMPUP={Parameters.rampup_jmeter} "
                          f"-J THROUGHPUT={Parameters.throughput_jmeter} "
                          f"-J STATUSCODE={Parameters.status_code_expected} "
                          f"-J TIME={Parameters.duration_jmeter} "
                          f"-J VALOR={Parameters.expected_value} "
                          f"-J ID={Parameters.parameter_id} "
                          f"-J MAINPATH={Parameters.current_path} ")

            else:
                os.system(f"call {Parameters.path_jmeter} -t {escenario_jmx} -l {result_jtl} " #-e -o {folder_dashboard} 
                          f"-J URL={Parameters.url_jmeter} "
                          f"-J USER={Parameters.users_jmeter} "
                          f"-J RAMPUP={Parameters.rampup_jmeter} "
                          f"-J THROUGHPUT={Parameters.throughput_jmeter} "
                          f"-J STATUSCODE={Parameters.status_code_expected} "
                          f"-J TIME={Parameters.duration_jmeter} "
                          f"-J VALOR={Parameters.expected_value} "
                          f"-J ID={Parameters.parameter_id} "
                          f"-J MAINPATH={Parameters.current_path} ")

    @staticmethod
    def clean_dashboard_folder(folder):

        """

                 Description:
                     Borra el contenido que tiene la carpeta que se pasa como parámetro

                 Args:
                     folder: ruta de la carpeta que se quiere borrar el contenido.

         """

        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    def generate_reports(self, file_input_report=Parameters.path_jmeter_report_jtl):

        """

            Description:
                Genera reporte de la ejecución actual utilizando JMeterPluginsCMD.bat.
                Genera:
                        AggrregateReport (.csv)
                        ResponseTimesOverTime (.png)
                        ResponseCodePerSecond (.png)
                        ThreadsStateOverTime (.png)

            Args:
                file_input_report: Path completo donde se encuentra report.jtl que va ser utilizado para generar el reporte.

        """

        path_bkp = os.getcwd()
        os.chdir(Parameters.path_jmeter_libraries_ext)
        os.system(f'call JMeterPluginsCMD.bat --generate-csv {Parameters.path_aggregate_report_csv_out} --input-jtl {file_input_report} --plugin-type AggregateReport')
        os.system(f'call JMeterPluginsCMD.bat --generate-png {Parameters.path_response_over_times_png_out} --input-jtl {file_input_report} --plugin-type ResponseTimesOverTime --relative-times no --width 800 --height 600')
        os.system(f'call JMeterPluginsCMD.bat --generate-png {Parameters.path_response_code_per_second_png_out} --input-jtl {file_input_report} --plugin-type ResponseCodesPerSecond --width 800 --height 600')
        os.system(f'call JMeterPluginsCMD.bat --generate-png {Parameters.path_response_threads_state_over_time} --input-jtl {file_input_report} --plugin-type ThreadsStateOverTime  --width 800 --height 600')
        os.chdir(path_bkp)

    @staticmethod
    def get_list_data_csv(file_csv):

        """

            Description:
                lee la ultima linea del csv generado y lee cada campo agregandolo en una lista.
                Genera:
                        Una lista con los campos obtenidos del csv.

            Args:
                file_csv: Path completo donde se encuentra csv generado actualmente.

            :returns: Devuelve lista de campos;

        """

        list_ready_csv = ""
        with open(file_csv, "r") as file_opened:
            next(file_opened, None)
            next(file_opened, None)
            for line in file_opened:
                list_ready_csv = line.split(",")
        return list_ready_csv

    @staticmethod
    def generate_html_table_description(file_csv):

        """

            Description:
                Genera un html con css con la descripción de la tabla csv que se genera al hacer una prueba de estrés.

            Args:
                file_csv: ruta del archivo csv.

            Returns:
                Devuelve un string en formato HTML/CSS con la descripción de la tabla csv.

        """

        list_data_csv = Functions.get_list_data_csv(file_csv)
        return f"""<html> <body> <font color = 'black'>
        <h5 style="text-align:center;">DESCRIPCIÓN DE LA TABLA:</h5>
        <p><strong>Samples ({list_data_csv[1]})</strong> = cantidad total de request hechas durante la prueba.</p>
        <p><strong>90% line ({list_data_csv[4]}ms)</strong> = el promedio del tiempo de respuesta en milisegundos considerando el 90% del total de la prueba.</p>
        <p><strong>Min ({list_data_csv[7]}ms)</strong>: el tiempo de respuesta más bajo de la prueba en milisegundos.</p>
        <p><strong>Max ({list_data_csv[8]}ms)</strong>: el tiempo de respuesta más alto de la prueba en milisegundos.</p>
        <p><strong>Error ({list_data_csv[9]})</strong>: porcentaje de error.</p>
        <p><strong>Throughput ({list_data_csv[10]})</strong>: promedio de request por minuto durante la prueba.</p>
        </ font> </ body> </ html>"""


    def attach_file_csv_with_description(self, file_csv, description):

        """

            Description:
                Agrega el archivo csv generado y su descripción al reporte allure.

            Args:
                file_csv: Path completo donde se encuentra csv generado.
                description: titulo que se agrega junto con el csv.

        """

        try:
            allure.attach.file(file_csv,description, attachment_type=allure.attachment_type.CSV, extension=".txt")

        except Exception as e:
            FunctionsGeneric.exception_logger(e)
            print(f"No se pudo cargar aggregate report")

        allure.attach(body=Functions.generate_html_table_description(file_csv), name="Descripcion tabla",
                      attachment_type=allure.attachment_type.HTML)



    @staticmethod
    def attach_file_png(file_png, description):

        """

            Description:
                Agrega el archivo csv generado y su descripción al reporte allure

            Args:
                file_png: Path completo donde se encuentra csv generado.
                description: titulo que se agrega junto con el csv.

        """
        responseOverTime = """<html> <body> <font color = 'black'>
        <h4 style="text-align:center;"> Gráfico que muestra los tiempos de respuesta a través del tiempo:</h4>
        <p><strong>EJE X:</strong> = refleja el tiempo.
        <p><strong>EJE Y:</strong> = refleja los tiempos de respuesta en milisegundos.
        </ font> </ body> </ html>"""

        ResponseCodePerSecond = """<html> <body> <font color = 'black'> <h4 style="text-align:center;">Gráfico que 
        muestra los status code y el número de respuestas por segundo a través del tiempo:</h4> <p><strong>EJE 
        X:</strong> = refleja el tiempo. <p><strong>EJE Y:</strong> = refleja el número de respuestas por segundo 
        durante la prueba. </ font> </ body> </ html> """

        ThreadsStateOverTime = """<html> <body> <font color = 'black'>
        <h4 style="text-align:center;">Gráfico que muestra la cantidad de usuarios que están activos durante el tiempo:</h4>
        <p><strong>EJE X:</strong> = refleja el tiempo.
        <p><strong>EJE Y:</strong> = refleja el número de usuarios activos durante la prueba.
        </ font> </ body> </ html>"""

        try:
            allure.attach.file(file_png,description,
                          attachment_type=allure.attachment_type.PNG,extension=".png")
        except Exception as e:
            FunctionsGeneric.exception_logger(e)
            print(f"No se pudo cargar grafico")

        if(description == "ResponseOverTime"):
            allure.attach(body=responseOverTime, name="Descripcion del gráfico",
                          attachment_type=allure.attachment_type.HTML)
        elif(description == "ResponseCodePerSecond"):
            allure.attach(body=ResponseCodePerSecond, name="Descripcion del gráfico",
                          attachment_type=allure.attachment_type.HTML)
        else:
            allure.attach(body=ThreadsStateOverTime, name="Descripcion del gráfico",
                          attachment_type=allure.attachment_type.HTML)

    @staticmethod
    def attach_file_jtl(description, file=Parameters.path_jmeter_report_jtl):

        """

            Description:
                Agrega archivo jtl y su descripción al reporte allure.

            Args:
                description: Nombre que va figurar en el reporte.
                file:  Path completo donde se encuentra report.jtl.

        """

        try:
            allure.attach.file(file, description, attachment_type=allure.attachment_type.CSV, extension=".txt")

        except Exception as e:
            FunctionsGeneric.exception_logger(e)
            print(f"No se pudo cargar archivo jtl")

        #allure.attach(body=Functions.generate_html_table_description(file), name="Descripcion archivo JTL",
        #             attachment_type=allure.attachment_type.HTML)

    @staticmethod
    @DeprecationWarning
    def validar_status_code_csv(file, expected_status):

        """

            Description:
                Se toma el resultado obtenido (.csv) y se valida el status code obtenido con el esperado.

            Args:
                file: Ubicación del archivo csv generado en la carpeta downloads.
                expected_status: Status code esperado.

        """

        #print(os.getcwd())
        with open(file, "r") as file_opened:
            next(file_opened, None)
            for line in file_opened:
                list_ready_csv = line.split(",")
                status_code = list_ready_csv[3]
                unittest.TestCase().assertEqual(str(expected_status), status_code,
                                                "El codígo de respuesta es diferente")

    @staticmethod
    def validate_expected_value(file, expected_value):

        """

            Description:
                Se toma el resultado obtenido (.csv) y se valida el valor esperado.

            Args:
                file: Ubicación del archivo csv generado en la carpeta downloads
                expected_value: Valor esperado.

        """

        with open(file, "r") as file_opened:
            next(file_opened, None)
            for line in file_opened:
                list_ready_csv = line.split(",")
                valor_actual = list_ready_csv[8]
                unittest.TestCase().assertFalse(valor_actual, f"el valor {expected_value} "
                                                              f"no se encuentra en el respose")
    @staticmethod
    def validate_percentage_errors(porcentaje_tolerado):

        """

            Description:
                Se toma el resultado obtenido (.csv) y se valida el porcentaje de error tolerado con el obtenido.

            Args:
                porcentaje_tolerado: porcentaje máximo tolerado por la prueba(float)

        """

        file_report = f"{Parameters.path_jmeter_downloads}\\AggregateReport.csv"

        with open(file_report, "r") as file_opened:
            next(file_opened, None)
            for line in file_opened:
                list_ready_csv = line.split(",")
                porcentaje_obtenido = list_ready_csv[9]

            print(f"porcentaje de errores: {porcentaje_obtenido}")
        with allure.step(f"PASO: Se valida que el porcentaje de error sea menor al {os.environ['errperc']}% de error"):
            unittest.TestCase().assertLessEqual(float(porcentaje_obtenido.replace("%", "")), float(porcentaje_tolerado),
                                                f"El porcentaje obtenido: {porcentaje_obtenido} es mayor al "
                                                f"tolerado: {porcentaje_tolerado}%")


    @staticmethod
    def validate_response_time(time_tolerado):

        """

            Description:
                Se toma el resultado obtenido (.csv) y se valida el tiempo de respuesta promedio tolerado de la prueba.

            Args:
                time_tolerado: tiempo máximo tolerado (float).

        """

        file_report = f"{Parameters.path_jmeter_downloads}\\AggregateReport.csv"

        with open(file_report, "r") as file_opened:
            next(file_opened, None)
            for line in file_opened:
                list_ready_csv = line.split(",")
                tiempo_response_obtenido = int(list_ready_csv[4])/1000
            print(f"tiempo de respuesta (90%): {tiempo_response_obtenido}")

        with allure.step(f"PASO: Se valida que el tiempo de respuesta sea menor a {os.environ['errtime']} segundos"):
            unittest.TestCase().assertLess(float(tiempo_response_obtenido), float(time_tolerado),
                                           f"El tiempo de respuesta obtenido: {round(tiempo_response_obtenido,2)} "
                                           f"es mayor al tolerado: {time_tolerado}")


    def create_and_get_path_report(self, name_file='report', extension_file='jtl'):

        """

            Description:
                Crea el archivo report.jtl por default si no se especifica name_file y extension_file.

            Args:
                name_file: Setea nuevo nombre de archivo sino por default es 'report'.
                extension_file: Setea nueva extension sino por default es 'jtl'

        """

        file_report = f"{Parameters.path_jmeter_downloads}\\{name_file}.{extension_file}"
        f = open(file_report, 'w')
        f.close()
        return file_report

    def get_path_escenario_jmx(self):

        """

            Description:
                Se obtiene la ruta del escenario jmx

            Returns:
                Devuelve la ruta del escenario jmx.

        """

        path_escenario_jmx = "..\\..\\files\\Escenarios\\" + self.class_name + "\\" + "API-PerformanceTest.jmx"

        return path_escenario_jmx


    def generate_html_data_params(self):

        """

            Description:
                Genera un HTML/CSS con los datos utilizados en la prueba.

            Returns:
                Devuelve un HTML/CSS con los datos utilizados en la prueba.

        """

        return f"""<html><body> <div>
        <h5>DATA UTILIZADA EN LA PRUEBA:</h5>
        <p><strong>URL</strong>: {self.data_resource['URL']}</p>
        <p><strong>Cantidad de Usuarios Virtuales</strong>: {os.environ['user']}</p>
        <p><strong>Tiempo de carga total de usuarios (segundos)</strong>: {os.environ['rampup']}</p>
        <p><strong>Throughput - request enviados por minuto</strong>: {os.environ['throughput']}</p>
        <p><strong>Tiempo de ejecución (minutos)</strong>: {os.environ['time']}</p>
        <p><strong>Status Code esperado</strong>: {self.data_resource["STATUSCODEESPERADO"]}</p>
        </div></body>"""+"""<style>
        h5{text-align: center;font-family: arial, sans-serif;font-size: 1.3em;font-weight: bold;}
        div{height:300px;background-color:#F5F5DC;border: 1px solid black;border-radius:25px;padding:20px;}
        </style></html>"""


    def attach_html_data_params(self):

        """

             Description:
                Adjunta un html con los parámetos usados en la prueba en un paso allure.

        """

        with allure.step(u"PASO: Datos utilizados en la prueba"):
            try:
                allure.attach(body=Functions.generate_html_data_params(self), name="Datos utilizados",
                          attachment_type=allure.attachment_type.HTML)
            except Exception as e:
                FunctionsGeneric.exception_logger(e)
                print(f"No se pudo cargar los datos utilizados")




