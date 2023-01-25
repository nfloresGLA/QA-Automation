# -*- coding: utf-8 -*-
import datetime
import os
import platform
import pprint
import random
import re
import string
import time
import allure
import cx_Oracle
import json
import unittest
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, NoSuchWindowException, \
    TimeoutException, StaleElementReferenceException, ElementClickInterceptedException, \
    ElementNotInteractableException, WebDriverException, UnexpectedAlertPresentException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.ie.options import Options as IeOptions
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager
from functions.Functions import Functions as GenericFunctions
from functions.Parameters import Parameters
if platform.system() == "Windows":
    from win32com.client import Dispatch
    from functions.Debugger import Debugger


class Functions(GenericFunctions, Parameters):
    windows = {}
    driver = None
    value_to_find = None
    get_locator_type = None
    number_windows = None
    exception = None
    json_strings = None
    complete_json_path = None
    message_container = None
    global_date = time.strftime(Parameters.date_format)  # formato dd/mm/aaaa
    global_time = time.strftime(Parameters.time_format)  # formato 24 houras
    lista_pasos = []
    lista_descripcion_pasos = []

    # INICIALIZA LOS DRIVER Y LOS CONFIGURA
    def open_browser(self, url=None, browser=Parameters.browser, options_headless=Parameters.headless,
                     download_path=None):

        """
            Description:
                Inicializa el navegador con las configuraciones definidas por el ambiente.
            Args:
                url: Url del Proyecto.
                browser: Navegador a utilizar.
                options_headless: True o False para utilizar el navegador en modo headless.
                download_path: Ruta a la carpeta de descargas.
            Returns:
                Retorna el driver e imprime por consola:
                    -El directorio base
                    -El navegador utilizado
        """

        print(f"Directorio Base: {Parameters.current_path}")
        print(f"Iniciando el navegador {browser}.")
        options = None
        if browser == "CHROME":
            options = ChromeOptions()
            if download_path is None:
                download_default = {"download.default_directory": self.path_downloads}
                options.add_experimental_option("prefs", download_default)
            else:
                options.add_experimental_option("prefs", {"download.default_directory": download_path})
        if browser == "FIREFOX":
            options = FirefoxOptions()
        if browser == "IE":
            options = IeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--incognito")
        options.add_argument("--enable-automation")
        options.add_argument("--disable-extensions")
        options.add_argument("--dns-prefetch-disable")
        options.add_argument("--verbose")
        options.add_argument("--disable-popup-blocking")
        #options.add_argument("--disable-extensions")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--disable-gpu") if os.name == "nt" else None
        if Parameters.environment == "Linux":
            options.add_argument("--headless")
            if browser == "CHROME":
                services = Service(r'/usr/bin/chromedriver')
                self.driver = webdriver.Chrome(service=services, options=options)
                self.set_mode_debug(False)
                self.initialize_browser(url)
                self.driver.maximize_window()
        if Parameters.environment == "Windows":
            if options_headless or Parameters.enviroment_confguration == "Server":
                options.add_argument("--headless")
                self.select_browser(browser, options)
                self.initialize_browser(url)
                self.set_highlight(False)
            else:
                self.set_mode_debug()
                self.select_browser(browser, options)
                self.initialize_browser(url)
                self.driver.maximize_window()
        return self.driver

    def initialize_browser(self, url):

        """
            Description:
                Inicia el navegador configurado y navega hacia la url.
            Args:
                url: Url destino.
        """

        self.driver.implicitly_wait(10)
        try:
            self.driver.get(url)
            self.windows = {'Principal': self.driver.window_handles[0]}

        except WebDriverException:
            Functions.tear_down(self)
            unittest.TestCase().fail(f"--WebDriverException--"
                                     f" No se ha podido establecer una conexion con el ambiente de pruebas '{url}'.")

    def select_browser(self, browser, options):

        """
            Description:
                Permite configurar el navegador que se utilizará en la prueba.
            Args:
                browser: Nombre del navegador.
                options: Argumentos opcionales del navegador.
        """

        driver_download_path = Parameters.current_path
        try:
            if browser == "CHROME":
                version = Functions.get_version_driver_for_browser(browser)
                services = Service(ChromeDriverManager(path=driver_download_path, version=version).install())
                self.driver = webdriver.Chrome(service=services, options=options)
            elif browser == "FIREFOX":
                services = Service(executable_path=GeckoDriverManager(path=driver_download_path).install(),
                                   log_path=None)
                self.driver = webdriver.Firefox(service=services, options=options)
            elif browser == "IE":
                services = IEDriverManager(path=driver_download_path).install()
                self.driver = webdriver.Ie(services)

        except WebDriverException as e:
            print(f"Ah ocurrido un problema. {e}")
            GenericFunctions.exception_logger(e)
            unittest.TestCase().skipTest("El web driver no esta disponible para esta prueba.")

        except Exception as e:
            print(f"Ah ocurrido un problema.")
            GenericFunctions.exception_logger(e)
            unittest.TestCase().skipTest("El web driver no esta disponible para esta prueba.")

    @staticmethod
    def get_version_driver_for_browser(browser):

        """
            Description:
                Detecta la versión del navegador que se está utilizando y descarga la versión del
                driver correspondiente.
            Args:
                browser: Nombre del navegador.
            Returns:
                version: Versión del navegador pasado como parametro en el argumento, si no encuentra el
                navegador instalado devuelve vacío y descarga la versión más actual del driver.
        """

        version = ""
        paths = []
        parser = Dispatch("Scripting.FileSystemObject")

        if browser == "CHROME":
            paths = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                     r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                     r"D:\Program Files\Google\Chrome\Application\chrome.exe",
                     r"D:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                     rf"C:\Users\{os.getlogin()}\AppData\Local\Google\Chrome\Application\chrome.exe"]
        for filename in paths:
            try:
                version = parser.GetFileVersion(filename)
                break
            except Exception as e:
                GenericFunctions.exception_logger(e)

        if version == "":
            return version

        if browser == "CHROME":
            version = f"{version.split('.')[0]}.{version.split('.')[1]}.{version.split('.')[2]}"
            response = requests.get(f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{version}")
            version = response.text

        return version

    @staticmethod
    def get_environment():

        """
            Description:
                Devuelve el environment (Sistema operativo) en el que se está corriendo la prueba.
        """

        return Parameters.environment

    def tear_down(self):

        """
            Descripcion:
                Finaliza la ejecución cerrando el Web Driver.
        """

        try:
            if self.data_cache not in ([], {}):
                print("Se utilizaron las siguientes variables...")
                pprint.pprint(self.data_cache)
            self.driver.quit()
            print("Se cerrará el DRIVER.")
            #############################################


        except Exception as e:
            GenericFunctions.exception_logger(e)

        finally:
            print(f"Finaliza la ejecución.")

    def refresh(self):

        """
            Description:
                Actualiza la página web.
        """

        self.driver.refresh()
        self.page_has_loaded()

    @staticmethod
    def set_browser(browser):

        """
            Description:
                Setea el navegador por defecto.
            Args:
                browser (str): Navegador.
        """

        Parameters.browser = browser
        print(f"El navegador seleccionado es: {str(Parameters.browser)}.")

    def get_proyect_name(self):

        """
            Description:
                Obtiene el nombre del proyecto en contexto.
            Returns:
                Retorna el nombre del proyecto en contexto.
        """

        project_name = os.path.abspath(str(self)).split(' ')[0].split('\\')[-4]
        return project_name

    # LOCALIZADORES ####################################################################################################
    def get_current_url(self):

        """
            Description:
                Obtiene la url actual de la pestaña activa.
            Returns:
                Url (str): La url de la pestaña activa.
        """

        return self.driver.current_url

    def locator_element(self, type_locator, indentify):

        """
            Description:
                Localiza un elemento utilizando el tipo de identificador indicado como parámetro.
            Args:
                type_locator: Tipo de identificador.
                indentify: Identificador.
            Returns:
                Si el elemento fue encontrado imprime "Esperar_Elemento: Se visualizó el elemento " + XPATH",
                en caso contrario imprime "No se pudo interactuar con el elemento", XPATH".
        """

        find_element = False
        elements = ""
        try:
            elements = self.driver.find_element(type_locator, indentify)
            print(f"Se interactuo con el elemento {indentify}")
            find_element = True

        except NoSuchElementException:
            self.exception = "NoSuchElementException"
            print(f"No se pudo interactuar con el elemento: {indentify}")

        except TimeoutException:
            self.exception = "TimeoutException"
            print(f"No se pudo cargar el elemento en el DOM agotando el tiempo de espera: {indentify}")

        except Exception as e:
            GenericFunctions.exception_logger(e)
            print(f"Ha ocurrido un error inesperado en tiempo de ejecución.")
        self.lista_descripcion_pasos.append(indentify)
        return elements, find_element

    def highlight(self, element: WebElement):

        """
            Description:
                Marca en pantalla el elemento pasado como parámetro.
            Args:
                element: Elemento al que se le hace foco.
        """

        Functions.wait(self, 1)
        try:
            original_style = element.get_attribute('style')
            highlight_style = "border: 3px solid green;"
            for x in range(2):
                try:
                    self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                               element, highlight_style)
                    time.sleep(0.1)
                    self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                               element, original_style)
                    time.sleep(0.1)

                except Exception as e:
                    GenericFunctions.exception_logger(e)
                    print(f"Se encontro el elemento pero no puede ser señalado.")

        except Exception as e:
            GenericFunctions.exception_logger(e)
            print(f"No se pudo señalar el elemento.")

    def capture_element(self, entity, variable_x=None, variable_y=None):

        """
            Description:
                Captura en pantalla la entidad pasada como parámetro.
            Args:
                entity: Entidad del objeto al que se quiere capturar en pantalla.
                variable_x: Variable x para parametrizar un elemento JSON.
                variable_y: Variable y para parametrizar un elemento JSON.
            Returns:
                Si la entidad se encuentra correctamente se devuelve el elemento y se imprime "Última screenshot
                antes de finalizar la ejecución", caso contrario lanza la excepción.
        """

        element = None
        Functions.page_has_loaded(self)
        get_entity = Functions.get_entity(self, entity)
        if get_entity is None:
            print("No se encontro el value en el Json definido.")
        else:
            if variable_x is not None:
                self.value_to_find = self.value_to_find.replace("IndiceX", variable_x)
            if variable_y is not None:
                self.value_to_find = self.value_to_find.replace("IndiceY", variable_y)

        find_element = False
        for intentos in range(Parameters.number_retries):
            if self.get_locator_type.lower() == "xpath":
                element, find_element = Functions.locator_element(self, By.XPATH, self.value_to_find)

            elif self.get_locator_type.lower() == "id":
                element, find_element = Functions.locator_element(self, By.ID, self.value_to_find)

            elif self.get_locator_type.lower() == "name":
                element, find_element = Functions.locator_element(self, By.NAME, self.value_to_find)
            else:
                print("El tipo de entidad del objeto no es valido para Selenium Framework.")
                unittest.TestCase().fail(f"--JsonErrorIdentity-- El tipo de entidad del objeto {entity} no es valido.")

            if find_element:
                unittest.TestCase().assertTrue(find_element, f"El elemento {entity} se visualiza en pantalla.")
                if Parameters.highlight:
                    Functions.highlight(self, element)
                else:
                    Functions.wait(self, Parameters.time_between_retries)
                break
            Functions.wait(self, Parameters.time_between_retries)

        if not find_element:
            if Functions.get_mode_execution() and not Functions.get_mode_browser():
                # captura
                self.image_for_debugger_report()
                self.steps_case = ""
                for i in range(len(self.lista_pasos)):
                    self.steps_case += f"* {self.lista_pasos[i]}: {self.lista_descripcion_pasos[i]}\n"
                status_code_returned = Functions.debugger(self, entity)
                if status_code_returned == 1:  # retry / refab
                    self.set_retry(3)
                    return self.capture_element(entity)
                if status_code_returned == 2:  # quit
                    return element
                if status_code_returned == 3:  # create Jira report
                    return element
                if status_code_returned == 4:  # reporte existente
                    self.set_retry(1)
            Functions.screenshot(self, "Ultima screenshot antes de finalizar la ejecución")
            unittest.TestCase().fail(f"--{self.exception}-- El objeto {entity} no se visualiza en pantalla.")

        return element

    def get_element(self, entity: object, variable_y: object = None, variable_x: object = None):

        """
            Description:
                Obtiene un elemento de un archivo json, según su identificador.
            Args:
                entity (str): Entidad del objeto que se quiere obtener.
                variable_y: Variable x para parametrizar un elemento JSON.
                variable_x: Variable y para parametrizar un elemento JSON.
            Returns:
                Si la entidad fue encontrada retorna el elemento, en caso contrario imprime
                "No se encontro el value en el Json definido".
        """

        element = Functions.capture_element(self, entity, variable_y=variable_y, variable_x=variable_x)

        class Element(Functions):

            def __init__(self, instance, context_element: WebElement, driver, json_value, json_get_indicator):
                self.retry = 0
                self.element = context_element
                self.driver = driver
                self.instance = instance
                self.json_ValueToFind = json_value
                self.json_GetFieldBy = json_get_indicator
                self.menssage = ""
                self.exception = None

            def click(self):
                self.execute_action("click")

            def click_js(self):
                self.execute_action("click_js")

            def double_click(self):
                self.execute_action("double_click")

            def send_keys(self, value):
                self.execute_action("send_keys", value)

            def send_special_key(self, value):
                self.execute_action("send_special_key", value)

            @property
            def text(self):
                return self.execute_action("text")

            def clear(self):
                self.execute_action("clear")

            def clear_js(self):
                self.execute_action("clear_js")

            def is_enabled(self):
                return self.execute_action("is_enabled")

            def is_selected(self, value):
                return self.execute_action("is_selected", value)

            def is_displayed(self):
                return self.execute_action("is_displayed")

            def get_property(self, value):
                return self.execute_action("get_property", value)

            def get_attribute(self, value):
                return self.execute_action("get_attribute", value)

            def capture(self):
                return self.execute_action("capture")

            def select_option_by_text(self, value):
                return self.execute_action("select_option_by_text", value)

            def select_option_by_value(self, value):
                return self.execute_action("select_option_by_value", value)

            def select_option_by_index(self, value):
                return self.execute_action("select_option_by_index", value)

            def get_all_values_to_select(self):
                return self.execute_action("get_all_values_to_select")

            def select_action(self, action, value=None):
                self.menssage = ""

                if action == "click":
                    self.menssage = "realizar click"
                    return self.element.click()

                if action == "click_js":
                    self.menssage = "realizar click"
                    self.driver.execute_script("arguments[0].click();", self.element)

                if action == "double_click":
                    self.menssage = "realizar doble click"
                    return Functions.double_click_element(self, self.element)

                if action == "send_keys":
                    self.menssage = "escribir en el campo"
                    return self.element.send_keys(value)

                if action == "send_special_key":
                    self.menssage = f"presionar la tecla {value} en el objetivo"
                    key = value.upper()
                    if key == 'ENTER':
                        self.element.send_keys(Keys.ENTER)
                    if key == 'TAB':
                        self.element.send_keys(Keys.TAB)
                    if key == 'ESPACIO':
                        self.element.send_keys(Keys.SPACE)
                    if key == 'ESCAPE':
                        self.element.send_keys(Keys.ESCAPE)
                    if key == 'RETROCESO':
                        self.element.send_keys(Keys.BACKSPACE)
                    if key == 'SUPRIMIR':
                        self.element.send_keys(Keys.DELETE)
                    if key == "ABAJO":
                        self.element.send_keys(Keys.ARROW_DOWN)

                if action == "text":
                    self.menssage = "obtener texto del campo"
                    return self.element.text

                if action == "clear":
                    self.menssage = "limpiar el texto del campo"
                    return self.element.clear()

                if action == "clear_js":
                    self.menssage = "limpiar campo"
                    self.driver.execute_script('arguments[0].value="";', self.element)

                if action == "is_enabled":
                    self.menssage = "verificar el estado del objeto"
                    return self.element.is_enabled()

                if action == "is_selected":
                    self.menssage = "verificar si el objeto es seleccionable"
                    return self.element.is_selected()

                if action == "is_displayed":
                    self.menssage = "visualizar el objeto"
                    return self.element.is_displayed()

                if action == "get_property":
                    self.menssage = "obtener las propiedades del objeto"
                    return self.element.get_property(value)

                if action == "get_attribute":
                    self.menssage = "obtener los atributos del objeto"
                    return self.element.get_attribute(value)

                if action == "capture":
                    self.menssage = "capturar pantalla"
                    Functions.highlight(self, self.element)
                    Functions.screenshot(self, f"Se visualiza el objeto {entity}")
                    return

                if action == "select_option_by_value":
                    self.menssage = f"seleccionar value {value} de la lista"
                    Select(self.element).select_by_value(value)

                if action == "select_option_by_text":
                    self.menssage = f"seleccionar value {value} de la lista"
                    Select(self.element).select_by_visible_text(value)

                if action == "select_option_by_index":
                    self.menssage = f"seleccionar value {value} de la lista"
                    Select(self.element).select_by_index(value)

                if action == "get_all_values_to_select":
                    list_value = []
                    self.menssage = f"obtener todos los valores de la lista {self.element}"
                    print(Select(self.element).options)
                    for option_value in Select(self.element).options:
                        list_value.append(option_value.get_attribute("value"))
                    return list_value

            def execute_action(self, action, value=None):
                out = None
                self.menssage = ""
                while self.retry <= Parameters.number_retries:
                    if self.retry < Parameters.number_retries:
                        try:
                            out = self.select_action(action, value)
                            break

                        except StaleElementReferenceException:
                            self.retry += 1
                            self.exception = "StaleElementReferenceException"
                            self.menssage = f'--{self.exception}-- No se ha podido {self.menssage} ' \
                                            f'debido a que el objeto "{entity}" a sido actualizado repentinamente.'
                            self.element = Functions.capture_element(self.instance, entity)

                        except ElementClickInterceptedException:
                            self.exception = "ElementClickInterceptedException"
                            self.retry = Parameters.number_retries
                            self.menssage = f'--{self.exception}-- No se ha podido {self.menssage} ' \
                                            f'debido a que el objeto "{entity}" se encuentra solapado por otro objeto.'

                        except ElementNotInteractableException:
                            self.retry += 1
                            self.exception = "ElementNotInteractableException"
                            self.menssage = f'--{self.exception}-- No se ha podido {self.menssage} ' \
                                            f'debido a que el objeto "{entity}" no esta disponible.'
                            self.element = Functions.capture_element(self.instance, entity)

                        except NoSuchElementException:
                            self.retry += 1
                            self.exception = "NoSuchElementException"
                            self.menssage = f'--{self.exception}-- No se ha podido {self.menssage} ' \
                                            f'debido a que el objeto "{entity}" no esta disponible.'
                            self.element = Functions.capture_element(self.instance, entity)

                        except Exception as e:
                            self.retry += 1
                            self.exception = str(e)
                            self.menssage = f'--{self.exception}-- No se ha podido {self.menssage} ' \
                                            f'debido a que ha ocurrido un error inesperado.'
                            self.element = Functions.capture_element(self.instance, entity)

                    else:
                        Functions.screenshot(self, "Ultima screenshot antes de finalizar la ejecución")
                        Functions.tear_down(self)
                        if len(self.menssage) == 0:
                            self.menssage = f"--{self.exception}-- {self.menssage}"
                        unittest.TestCase().fail(self.menssage)
                Functions.message_container = self.menssage
                self.lista_pasos.append(action)
                return out

        Functions.page_has_loaded(self)
        return Element(self, element, self.driver, self.value_to_find, self.get_locator_type)

    def debugger(self, debug_this_entity):

        """
            Description:
                Permite visualizar los defectos antes de finalizar la ejecución, la corrección de los mismos y
                luego cierra el navegador.
            Args:
                debug_this_entity: Nombre de la entidad en conflicto.
            Returns:
                Devuelve el status code correspondiente a la acción realizada por el usuario dentro de la UI.
        """

        # La función fixer devuelve status Code, el nuevo xpath, id o name que actualiza la variable en memoria
        returned_code, self.value_to_find, self.get_locator_type = Debugger(self, debug_this_entity, self.exception,
                                                                            self.get_locator_type,
                                                                            self.value_to_find,
                                                                            self.complete_json_path,
                                                                            self.json_strings,
                                                                            self.case_name).fixer()
        if returned_code == 1:
            return 1
        if returned_code == 2:
            return 2
        if returned_code == 3:
            unittest.TestCase().fail("Incidencia reportada")
        if returned_code == 4:
            unittest.TestCase().fail("Incidencia reportada")

    def get_json_file(self, file):

        """
            Description:
                Lee un archivo json.
            Args:
                file (file): Archivo json.
            Returns:
                Si el archivo fue encontrado imprime "get_json_file: " + json_path",
                en caso contrario imprime "get_json_file: No se encontro el Archivo " + file".
        """

        json_path = os.path.join(self.path_json, f"{file}.json")
        self.complete_json_path = json_path
        try:
            with open(json_path, "r", encoding='utf8') as read_file:
                self.json_strings = json.loads(read_file.read())
                print("get_json_file: " + json_path)
        except FileNotFoundError:
            self.json_strings = False
            unittest.TestCase().skipTest(u"get_json_file: No se encontro el Archivo " + file)
            Functions.tear_down(self)

    def get_entity(self, entity):

        """
            Description:
                Lee una entidad del archivo json.
            Args:
                entity (str): Entidad del objeto que se quiere leer.
            Returns:
                Si la entidad fue encontrada retorna "True", en caso contrario imprime
                "get_entity: No se encontró la key a la cual se hace referencia: " + entity".
        """

        if not self.json_strings:
            print("Define el DOM para esta prueba")
        else:
            try:
                self.value_to_find = self.json_strings[entity]["ValueToFind"]
                self.get_locator_type = self.json_strings[entity]["GetFieldBy"]

            except KeyError as e:
                GenericFunctions.exception_logger(e)
                unittest.TestCase().skipTest(f"get_entity: No se encontro la key a la cual se hace referencia:"
                                             f"{entity}.")
                Functions.tear_down(self)

            return True

    # TEXTBOX & COMBO HANDLE ###########################################################################################
    def send_especific_keys(self, element, key):

        """
            Description:
                Simula el envío de una tecla del teclado.
            Args:
                element (str): Entidad del objeto que se quiere obtener.
                key (str): Tecla seleccionada.
        """

        if key == 'Enter':
            Functions.get_element(self, element).send_keys(Keys.ENTER)
        if key == 'Tab':
            Functions.get_element(self, element).send_keys(Keys.TAB)
        if key == 'Space':
            Functions.get_element(self, element).send_keys(Keys.SPACE)
        if key == 'Esc':
            Functions.get_element(self, element).send_keys(Keys.ESCAPE)
        if key == 'Retroceso':
            Functions.get_element(self, element).send_keys(Keys.BACKSPACE)
        if key == 'Suprimir':
            Functions.get_element(self, element).send_keys(Keys.DELETE)
        if key == "Abajo":
            Functions.get_element(self, element).send_keys(Keys.ARROW_DOWN)
        time.sleep(3)

    def get_id_window(self):

        """
            Description:
                Obtiene el id de una window.
            Returns:
                Devuelve el id de la window obtenida.
        """

        print(self.driver.window_handles[0])
        return self.driver.window_handles[0]

    def switch_to_windows_handles(self, number_window):

        """
            Description:
                Cambia entre ventanas del navegador.
            Args:
                number_window (int): Número de window seleccionada.
        """

        self.driver.switch_to.window(self.driver.window_handles[number_window])
        self.driver.maximize_window()

    def switch_to_iframe(self, locator):

        """
            Description:
                Cambia entre iframes en la WebApp.
            Args:
                locator (str): Nombre del objeto que se quiere obtener.
            Returns:
                Imprime "Se realizó el switch a (Locator)".
        """

        iframe = Functions.capture_element(self, locator)
        self.driver.switch_to.frame(iframe)
        print(f"Se realizó el switch a {locator}")

    def switch_to_parent_frame(self):

        """
            Description:
                Cambia al iframes padre.
        """

        self.driver.switch_to.parent_frame()
        print(f"Se realizó el switch al parent frame.")

    def switch_to_default_frame(self):

        """
            Description:
                Cambia al iframe principal.
        """

        self.driver.switch_to.default_content()
        print(f"Se realizó el switch al frame principal.")

    def switch_to_windows_name(self, window):

        """
            Description:
                Cambia entre ventanas del navegador a través de su nombre.
            Args:
                window (str): Nombre de ventana seleccionada.
            Returns:
                Si la ventana es encontrada imprime "volviendo a (ventana)",
                en caso contrario imprime "Estas en (ventana)".
        """

        if window in self.windows:
            self.driver.switch_to.window(self.windows[window])
            Functions.page_has_loaded(self)
            print("volviendo a " + window + " : " + self.windows[window])
        else:
            self.number_windows = len(self.driver.window_handles) - 1
            self.windows[window] = self.driver.window_handles[int(self.number_windows)]
            self.driver.switch_to.window(self.windows[window])
            self.driver.maximize_window()
            print(self.windows)
            print("Estas en " + window + " : " + self.windows[window])
            Functions.page_has_loaded(self)

    def get_element_shadow_root(self, entity, index=0) -> WebElement:

        """
            Description:
                Obtiene el DOM del Shadow Root.
            Args:
                index: Índice seteado en 0.
                entity: Entidad del objeto que se quiere obtener.
            Returns:
                El DOM del Shadow Root.
        """

        element = self.get_element(entity)
        shadow_elements = self.driver.execute_script(f'return arguments[{index}].shadowRoot', element)
        return shadow_elements

    def close_page(self):

        """
            Description:
                Cierra la instancia del explorador.
        """

        self.driver.close()

    # FUNCIONES DE JAVASCRIPT ##########################################################################################
    def get_page_dom(self):

        """
            Description:
                Obtiene el DOM de una WebApp.
            Returns:
                El DOM de una WebApp.
        """

        return self.driver.execute_script("return document.documentElement.outerHTML")

    def new_window(self, url):

        """
            Description:
                Abre una nueva window con el navegador.
            Args:
                url (str): Dirección web que se debe cargar en la window
        """

        self.driver.execute_script(f'''window.open("{url}","_blank");''')
        Functions.page_has_loaded(self)

    def page_has_loaded(self):

        """
            Description:
                Espera que la página sea cargada.
            Returns:
                Si la página se cargó imprime "complete", en caso contrario imprime "No se completó la carga".
        """

        try:
            driver_target = self.driver
            print("Checking if {} page is loaded.".format(self.driver.current_url))
            page_state = driver_target.execute_script('return document.readyState;')
            yield
            WebDriverWait(driver_target, 30).until(lambda target: page_state == 'complete')
            assert page_state == 'complete', "No se completo la carga"

        except TimeoutException:
            unittest.TestCase().fail("--TimeoutException-- No se ha podido realizar la carga de la página.")

    def scroll_to(self, locator, y=None, x=None):

        """
            Description:
                Hace scroll en la página hacia el elemento que se pasa como parámetro.
            Args:
                y: Variable y para parametrizar un elemento JSON.
                x: Variable x para parametrizar un elemento JSON.
                locator (str): Nombre del elemento al cual se quiere scrollear.
        """

        element = Functions.capture_element(self, locator, variable_y=y, variable_x=x)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        print(f"Scroleando la pagina hacia el objeto: {locator}")

    # FUNCIONES DE ESPERA ##############################################################################################
    def wait(self, time_load, logger=Parameters.loggin_time, reason=None):

        """
            Description:
                Espera un elemento, el tiempo es dado en segundos.
            Args:
                time_load: Tiempo en segundos.
                logger:
                reason: Razón por la que se quiere esperar un elemento.
            Returns:
                Cuando termina el tiempo de espera imprime "Esperar: Carga Finalizada ... "
        """

        return GenericFunctions.wait(self, time_load, logger=logger, reason=reason)

    def alert_windows(self, accept="accept"):

        """
            Description:
                Espera un alert(window pop up) y hace click en accept.
            Args:
                accept (str): Opción aceptar.
            Returns:
                Al hacer click en accept imprime "Click in Accept", de lo contrario
                imprime "Alerta no presente".
        """

        try:
            wait = WebDriverWait(self.driver, 30)
            wait.until(ec.alert_is_present(), print("Esperando alerta..."))

            alert = self.driver.switch_to.alert

            if accept.lower() == "accept":
                alert.accept()
                print("Click in Accept")
            elif accept.lower() == "text":
                print("Get alert text")
                return alert.text
            else:
                alert.dismiss()
                print("Click in Dismiss")

        except NoAlertPresentException:
            print('Alerta no presente.')
        except NoSuchWindowException:
            print('Alerta no presente.')
        except TimeoutException:
            print('Alerta no presente.')
        except UnexpectedAlertPresentException:
            print('Alerta inesperada.')
        except Exception as e:
            GenericFunctions.exception_logger(e)
            print(f"Ocurrio un error inesperado.")

    # ACCION CHAINS ####################################################################################################
    def mouse_over(self, locator):

        """
            Description:
                Posiciona el mouse sobre un elemento.
            Args:
                locator (str): Locator del objeto que se quiere obtener.
            Returns:
                Retorna "True" si existe el objeto dentro del json, de lo contrario
                imprime "No se encontró el value en el Json definido".
        """

        get_entity = Functions.get_entity(self, locator)
        if get_entity is None:
            return print("No se encontro el value en el Json definido.")
        else:
            try:
                if self.get_locator_type.lower() == "id":
                    localizador = self.driver.find_element(By.ID, self.value_to_find)
                    action = ActionChains(self.driver)
                    action.move_to_element(localizador)
                    action.click(localizador)
                    action.perform()
                    print(u"mouse_over: " + locator)
                    return True

                if self.get_locator_type.lower() == "xpath":
                    localizador = self.driver.find_element(By.XPATH, self.value_to_find)
                    action = ActionChains(self.driver)
                    action.move_to_element(localizador)
                    action.click(localizador)
                    action.perform()
                    print(u"mouse_over: " + locator)
                    return True

                if self.get_locator_type.lower() == "link":
                    localizador = self.driver.find_element(By.PARTIAL_LINK_TEXT, self.value_to_find)
                    action = ActionChains(self.driver)
                    action.move_to_element(localizador)
                    action.click(localizador)
                    action.perform()
                    print(u"mouse_over: " + locator)
                    return True

                if self.get_locator_type.lower() == "name":
                    localizador = self.driver.find_element(By.NAME, self.value_to_find)
                    action = ActionChains(self.driver)
                    action.move_to_element(localizador)
                    action.click(localizador)
                    action.perform()
                    print(u"mouse_over: " + locator)
                    return True

            except TimeoutException:
                print(u"mouse_over: No presente " + locator)
                Functions.tear_down(self)
                return None

            except StaleElementReferenceException:
                print(u"element " + locator + " is not attached to the DOM")
                Functions.tear_down(self)
                return None

    def double_click_element(self, element: WebElement):

        """
            Description:
                Hace doble click con el mouse sobre un elemento.
            Args:
                element: Nombre del elemento que se quiere obtener.
        """

        mouse_action = ActionChains(self.driver)
        mouse_action.double_click(element)
        mouse_action.perform()

    def drag_and_drop(self, origin_object, target_object):

        """
            Description:
                Arrastra y suelta un elemento con el mouse.
            Args:
                origin_object (str): Origen del elemento.
                target_object (str): Destino del elemento.
        """

        ActionChains(self.driver).drag_and_drop(origin_object, target_object).perform()

    def click_and_hold(self, origin_object, target_object):

        """
            Description:
                Mantiene un elemento clickeado.
            Args:
                origin_object (str): Origen del elemento.
                target_object (str): Destino del elemento.
        """

        mouse_action = ActionChains(self.driver)
        mouse_action.click_and_hold(origin_object).move_to_element(target_object).release(target_object)
        mouse_action.perform()

    # VALIDADORES ######################################################################################################
    def check_element(self, locator):  # devuelve true o false

        """
            Description:
                Verifica si existe un objeto dentro del json.
            Args:
                locator (str): Nombre del objeto que se quiere verificar.
            Returns:
                Retorna "True" si existe el objeto dentro del json, de lo contrario
                imprime "No se encontro el value en el Json definido".
        """

        get_entity = Functions.get_entity(self, locator)

        if get_entity is None:
            print("No se encontro el value en el Json definido")
        else:
            try:
                if self.get_locator_type.lower() == "id":
                    wait = WebDriverWait(self.driver, 20)
                    wait.until(ec.visibility_of_element_located((By.ID, self.value_to_find)))
                    print(u"check_element: Se visualizo el elemento " + locator)
                    return True

                if self.get_locator_type.lower() == "name":
                    wait = WebDriverWait(self.driver, 20)
                    wait.until(ec.visibility_of_element_located((By.NAME, self.value_to_find)))
                    print(u"check_element: Se visualizo el elemento " + locator)
                    return True

                if self.get_locator_type.lower() == "xpath":
                    wait = WebDriverWait(self.driver, 20)
                    wait.until(ec.visibility_of_element_located((By.XPATH, self.value_to_find)))
                    print(u"check_element: Se visualizo el elemento " + locator)
                    return True

                if self.get_locator_type.lower() == "link":
                    wait = WebDriverWait(self.driver, 20)
                    wait.until(ec.visibility_of_element_located((By.LINK_TEXT, self.value_to_find)))
                    print(u"check_element: Se visualizo el elemento " + locator)
                    return True

                if self.get_locator_type.lower() == "css":
                    wait = WebDriverWait(self.driver, 20)
                    wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, self.value_to_find)))
                    print(u"check_element: Se visualizo el elemento " + locator)
                    return True

            except NoSuchElementException:
                print("get_text: No se encontró el elemento: " + self.value_to_find)
                return False
            except TimeoutException:
                print("get_text: No se encontró el elemento: " + self.value_to_find)
                return False

    # FUNCIONES DE CONFIGURACIÓN #######################################################################################

    def set_proyect(self, project_name=None):

        """
            Description:
                Setea variables de ambiente y rutas del proyecto.
            Args:
                project_name: Nombre del proyecto.
            Returns:
                Imprime por consola la siguiente configuración:
                    -Ambiente
                    -Ruta de Resource
                    -Ruta de Evidencias
                    -Ruta de los Json
                    -Ruta de las Imágenes de los json (reconocimiento por imágenes)
                    -Ruta de los Bass
                Si hubo un error en la configuración, imprime por consola
                "No se pudieron detectar los datos de la ejecución".
        """

        GenericFunctions.set_proyect(self, project_name)

    @staticmethod
    def set_env(env):

        """
            Descripcion:
                Configura una variable para la lectura de resources.

            Args:
                env: QA, TEST, PROD, ALT

            Returns:
                Funcion que configura la variable de ambiente para la lectura del resources

        """
        return GenericFunctions.set_env(env)



    @staticmethod
    def get_excel_row():

        """
            Description:
                Obtiene la row actual del excel.
            Returns:
                Imprime por consola "El numero del registro consultado es: "+ str(row)" y retorna la row.
        """

        return GenericFunctions.get_row_excel()

    def set_restore_excel_row(self):

        """
            Description:
                Restaura al value inicial el número de filas del excel.
            Returns:
                Imprime por consola "Se ha restarudado el numero de la row excel: "+ str(Parameters.row).
        """

        GenericFunctions.set_restore_excel_row()

    @staticmethod
    def set_increment_excel_row():

        """
            Description:
                Incrementa en 1 el número de filas del excel.
        """

        Parameters.manual_increment = True
        GenericFunctions.set_increment_row()

    @staticmethod
    def get_current_time():

        """
            Description:
                Se obtiene la hora actual.
            Returns:
                Retorna la hora actual.
        """

        return time.strftime(Parameters.time_format)  # formato 24 horas

    @staticmethod
    def get_retry():

        """
            Description:
                Se obtiene la cantidad de reintentos por default
            Returns:
                Retorna (int) la cantidad de reintentos por default
        """

        return Parameters.number_retries

    @staticmethod
    def set_highlight(value=True):

        """
            Description:
                Desactivar/activar el señalamiento highlight de la funcion get_element.
            Args:
                value: Valor booleano (seteado por default en True).
        """

        Parameters.highlight = value
        print(f"La opcion hightlight de get_element se a configurado en el siguiente value {Parameters.highlight}")

    def set_retry(self, numbers_retries):

        """
            Description:
                Se configura la cantidad de reintentos por default.
            Args:
                numbers_retries: Número entero que se utilizará como nuevo parámetro para
                la búsqueda de reintentos de objetos en el DOM.
        """

        GenericFunctions.set_retry(self, numbers_retries)

    @staticmethod
    def get_timeout_beetwen_retrys():

        """
            Description:
                Se obtiene el tiempo por default de espera entre reintentos.
            Returns:
                Retorna (int) el tiempo por default de espera entre reintentos.
        """

        return Parameters.time_between_retries

    @staticmethod
    def set_timeout_beetwen_retrys(time_target):

        """
            Description:
                Se configura el tiempo por default de espera entre reintentos.
            Args:
                time_target: Nímero entero que se utilizará para configurar el tiempo de espera entre reintentos.
        """

        Parameters.time_between_retries = time_target
        print(f"El tiempo de espera entre reintentos es {Parameters.time_between_retries}.")

    @staticmethod
    def get_mode_execution():

        """
            Description:
                Indica si el caso requiere ser debugeado.
            Returns:
                Devuelve valor de la variable de Parameters.debug (True o False)
                que indica si el caso requiere ser debugeado.
        """

        return Parameters.debug

    @staticmethod
    def set_mode_debug(status=True):

        """
            Description:
                Configura la variable Parameters.debug en verdadero.
            Args:
                status: Estado actual del debuger (True = Activado y False = Desactivado).
        """

        Parameters.debug = status

    @staticmethod
    def get_mode_browser():

        """
            Description:
                Obtiene la configuración del headless del navegador.
            Returns:
                Devuelve la configuración del navegador (Headless ON/True o Headless OFF/False).
        """

        return Parameters.headless

    @staticmethod
    def set_mode_browser(status=True):

        """
            Description:
                Setea el headless del navegador.
            Args:
                status: Estado actual del modo headless del browser (True = Activado y False = Desactivado).
        """

        Parameters.debug = status

    def read_cell(self, cell, case_name=None, specific_sheet=None) -> object:

        """
            Description:
                Lee la cell de un resource.
            Args:
                cell: Celda del resource.
                case_name: Nombre del caso.
                specific_sheet: Hoja del resource.
            Returns:
                Retorna el value de la cell del resource.
        """

        return GenericFunctions.read_cell(self, cell, file_name=case_name, specific_sheet=specific_sheet)

    # CAPTURA DE PANTALLA ##############################################################################################
    def crear_path(self):

        """
            Description:
                Se crea el directorio para las capturas de pantalla.
            Returns:
                Retorna el directorio creado.
        """

        day = time.strftime("%d-%m-%Y")  # formato aaaa/mm/dd
        general_path = self.path_evidences
        browser = Parameters.browser
        test_case = self.__class__.__name__
        current_time = time.strftime(Parameters.time_format)  # formato 24 houras
        x = re.search("Context", test_case)
        if x:
            path = f"{general_path}/{day}/{browser}/{current_time}/"
        else:
            path = f"{general_path}/{day}/{test_case}/{browser}/{current_time}/"

        if not os.path.exists(path):  # si no existe el directorio lo crea
            os.makedirs(path)

        return path

    def screenshot(self, description):

        """
            Description:
                Saca screenshot de pantalla para los reportes de allure y se agrega la descripción de la misma.
            Args:
                description: Descripción de la screenshot de pantalla.
            Returns:
                Retorna la imágen y descripción de la screenshot de pantalla.
        """

        try:
            allure.attach(self.driver.get_screenshot_as_png(), description, attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            GenericFunctions.exception_logger(e)
            print(f"No se pudo realizar la screenshot de pantalla.")


    def image_for_debugger_report(self):

        """
            Description:
                Saca screenshot de pantalla para los reportes de allure y se agrega la descripción de la misma.
            Args:
                description: Descripción de la screenshot de pantalla.
            Returns:
                Retorna la imágen y descripción de la screenshot de pantalla.
        """
        try:
            base_folder = f"C:\\testing-Automation\\projects\\{str(self.project_name)}\\src\\outputs\\"
            if "jira_report.png" not in base_folder:
                self.memory_image = self.driver.get_screenshot_as_png()
        except Exception as e:
            print(f"Hubo inconvenientes al intentar crear la carpeta contenedora de las 'report image'")






    # SERVICIOS WEB ####################################################################################################
    def send_service(self, data):

        """
            Description:
                Envía un servicio.
            Args:
                data: recibe los siguientes parámetros en formato json:
                    tipoPeticion (str): Tipo de petición del servicio.
                    endPoint (str): Endpoint del servicio.
                    headers (str): Headers del servicio.
                    payload (str): Payload del servicio.
                    time (int): Tiempo de espera de la respuesta del servicio.
                    statusCodeEsperado (int): Codigo de estatus esperado en la respuesta.
                    responseEsperado: (dict_to_json):
            Returns:
                Retorna un request si la petición es exitosa y un array con las
                diferencias obtenidas. De lo contrario imprime el error por consola.
        """

        response = ""
        validation_structure = "None"
        differences = []
        validate_cant_records = "None"
        cant_registros_db = ""
        cant_registros_api = ""
        statuscode = None
        validation_status_code = None

        total_retry = Parameters.number_retries

        # Se realiza el llamado a la api, si falla reintenta nuevamente.
        for retry in range(total_retry):
            if data['headers'] is not None:
                try:
                    response = requests.request(data['tipoPeticion'], data['endPoint'], headers=data['headers'],
                                                data=data['payload'], timeout=data['time'])
                    print(f"El servicio '{data['endPoint']}' respondio con status code {response.status_code}")
                    break
                except requests.exceptions.Timeout:
                    print("Hubo un error por timeout al enviar el servicio")
            else:
                try:
                    response = requests.request(data['tipoPeticion'], data['endPoint'], timeout=data['time'])
                    print(f"El servicio '{data['endPoint']}' respondio con status code {response.status_code}")
                    break
                except requests.exceptions.Timeout:
                    print("Hubo un error por timeout al enviar el servicio")
            Functions.wait(self, 1)

        # Se valida es status code del request.
        try:
            validation_status_code = self.validate_status_code(data['statusCodeEsperado'], response.status_code)
            statuscode = response.status_code
        except AttributeError as e:
            GenericFunctions.exception_logger(e)
            print(f"Error al obtener el status code del servicio.")

        # Se valida la estructura/integridad del response.
        if 'validateStructure' in data.keys():
            if data['validateStructure']:
                validation_structure, differences = self.validate_structure(data['responseEsperado'], response)
            else:
                validation_structure = "None"

        # Se compara la cantidad de registros entre la DB y la API.
        if 'validateCantData' in data.keys():
            if data['validateCantData']:
                validate_cant_records, cant_registros_db, cant_registros_api = \
                    self.validate_cant_records(data, response)
            else:
                validate_cant_records = "None"
                cant_registros_db = "None"
                cant_registros_api = "None"

        # Se adjuntan las validaciones en formato HTML o formato JSON.
        if 'attach_validations' in data.keys():
            if data['attach_validations']:

                # Se imprime en el template los datos utilizados para las validaciones.
                if 'test_data' in data.keys():
                    data_validations = {
                        'precondition_data': data['test_data'],
                        'validations': [
                            {
                                'validation': 'Status code esperado',
                                'result': validation_status_code,
                                'status_code_esperado': data['statusCodeEsperado'],
                                'status_code_obtenido': response.status_code
                            },
                            {
                                'validation': 'Cantidad de registros',
                                'result': validate_cant_records,
                                'cantidad_datos_origen': cant_registros_db,
                                'cantidad_datos_destino': cant_registros_api
                            },
                            {
                                'validation': 'Estructura del response',
                                'result': validation_structure,
                                'differences': differences
                            }
                        ]
                    }
                else:
                    data_validations = {
                        'validations': [
                            {
                                'validation': 'Status code esperado',
                                'result': validation_status_code,
                                'status_code_esperado': data['statusCodeEsperado'],
                                'status_code_obtenido': response.status_code
                            },
                            {
                                'validation': 'Cantidad de registros',
                                'result': validate_cant_records,
                                'cantidad_datos_origen': cant_registros_db,
                                'cantidad_datos_destino': cant_registros_api
                            },
                            {
                                'validation': 'Estructura del response',
                                'result': validation_structure,
                                'differences': differences
                            }
                        ]
                    }

                # Formato de template que se adjunta en Allure.
                if 'template' in data.keys():
                    file = self.create_file_validations(data_validations, data['template'])
                else:
                    file = self.create_file_validations(data_validations, 'cards')

                # Se adjunta el archivo HTML en un step de Allure existente o nuevo.
                if 'step_allure' in data.keys():
                    if data['step_allure']:
                        with allure.step(u"PASO: Se realizan las siguientes validaciones"):
                            allure.attach.file(file, name="Validaciones", attachment_type=None, extension=".html")
                    else:
                        allure.attach.file(file, name="Validaciones", attachment_type=None, extension=".html")
                else:
                    allure.attach.file(file, name="Validaciones", attachment_type=None, extension=".html")

                # Se realizan los asserts de las validaciones.
                for i in range(len(data_validations['validations'])):
                    validataion = data_validations['validations'][i]['validation']
                    result = data_validations['validations'][i]['result']
                    if validataion == "Status code esperado" and not result:
                        unittest.TestCase().assertEqual(data['statusCodeEsperado'], response.status_code,
                                                        f"El status code no es el esperado, el value obtenido es "
                                                        f"{response.status_code}")

                    elif validataion == "Cantidad de registros" and not result:
                        unittest.TestCase().assertEqual(cant_registros_db, cant_registros_api,
                                                        "No coinciden la cantidad de datos entre origen y destino.")

                    elif validataion == "Estructura del response" and not result:
                        unittest.TestCase().assertEqual(len(differences), 0,
                                                        "Se encontraron differences en la estructura del response.")

                data_validations.clear()
            else:
                dict = {
                    'status_code_esperado': data['statusCodeEsperado'],
                    'status_code_obtenido': statuscode
                }
                self.attach_json(dict)
        else:
            dict = {
                'status_code_esperado': data['statusCodeEsperado'],
                'status_code_obtenido': statuscode
            }
            self.attach_json(dict)

        return response, differences

    @staticmethod
    def validate_status_code(status_code_esperado, status_code_obtenido):

        """
            Description:
                Se valida el status code de un servicio.
            Args:
                status_code_esperado (int): Código de estado esperado en la respuesta.
                status_code_obtenido (int): Código de estado obtenido en la respuesta.
            Returns:
                Retorna un booleano con el resultado de la validación.
        """

        if status_code_esperado == status_code_obtenido:
            validation = True
        else:
            validation = False
        return validation

    def validate_cant_records(self, data, response):

        """
            Description:
                Se valida la cantidad de registros de un servicio.
            Args:
                data: Diccionario con tados de DB.
                response: Response obtenido en la respuesta.
            Returns:
                Retorna un booleano con el resultado de la validación.
                Retorna la cantidad de datos obtenidos del origen y destino.
        """

        cant_registros_api = 0
        response = json.loads(response.text)

        # Se obtiene cantidad de datos existentes en la DB.
        cant_registros_db = self.check_base_sqlserver(data['data_db']['server'], data['data_db']['base'],
                                                      data['data_db']['user'], None, data['data_db']['consulta'])
        if len(cant_registros_db) > 0:
            cant_registros_db = cant_registros_db[0]

        # Se obtiene cantidad de datos existentes de la API.
        # Se debe pasar una 'key' del response obtenido para que cuente la cantidad de registros devueltos por la API.
        if str(type(response)) != "<class 'dict'>":
            for i in range(len(response)):
                if data['searchKey'] in response[i]:
                    cant_registros_api = cant_registros_api + 1
        else:
            if data['searchKey'] in response:
                cant_registros_api = cant_registros_api + 1

        if cant_registros_db == cant_registros_api:
            validation = True
        else:
            validation = False

        print(f"Cantidad de datos obtenidos desde la DB: {cant_registros_db}")
        print(f"Cantidad de datos obtenidos desde la API: {cant_registros_api}")

        return validation, cant_registros_db, cant_registros_api

    def validate_structure(self, expected_response, response_obtained):

        """
            Description:
                Se valida la estructura de un servicio.
            Args:
                expected_response: Diccionario con la estructura del response esperado.
                response_obtained: Diccionario con la estructura del response obtenido.
            Returns:
                Retorna un booleano con el resultado de la validación.
                Retorna un array con las diferencias encontradas.
        """

        diferencias = self.compare_structure(expected_response, response_obtained)

        if len(diferencias) == 0:
            validation = True
        else:
            validation = False

        print(f"Response esperado: {expected_response}")
        print(f"Response obtenido: {response_obtained.text}")

        return validation, diferencias

    @staticmethod
    def compare_structure(expected_response, response_obtained):

        """
            Description:
                Compara estructuras de una respuesta esperada con una respuesta obtenida de un servicio.
            Args:
                expected_response: Respuesta esperada en formato json.
                response_obtained: Respuesta obtenida en formato json.
            Returns:
                Retorna un array con las diferencias encontradas.
        """

        differences = []
        try:

            response_obtained = json.loads(response_obtained.text)
            unittest.TestCase().assertNotEqual(str(type(response_obtained)), "<class 'str'>", "Error: El response obtenido es de tipo String")
        except ValueError:
            unittest.TestCase().assertEqual(True, False, "Error al convertir el json value_text en diccionario.")

        if len(expected_response) > 0 and str(type(expected_response)) != "<class 'dict'>":
            expected_response = expected_response[0]

        if len(response_obtained) > 0 and str(type(response_obtained)) != "<class 'dict'>":
            response_obtained = response_obtained[0]

        # Busca y compara las key del json1 en json2.
        for key in expected_response:
            if key not in response_obtained.keys():
                error = {
                    'description': 'Keys que se encuentran en origen pero no en destino',
                    'missing_key': key
                }
                differences.append(error)

        # Busca y compara las key del json2 en json1.
        for key in response_obtained:
            if key not in expected_response.keys():
                error = {
                    'description': 'Keys que se encuentran en destino pero no en origen',
                    'missing_key': key
                }
                differences.append(error)

        return differences

    def create_file_validations(self, data_validations, name_template):

        """
            Description:
                Crea un archivo html con las validaciones realizadas.
            Args:
                data_validations (dict): Diccionario con información de las validaciones realizadas.
                name_template (str): Nombre del template a utilizar.
            Return:
                Retorna la ruta del archivo html creado.
        """

        from datetime import datetime
        replacement = ""
        path = self.path_output

        date_time = datetime.now().strftime("%d-%m-%y_%H-%M-%S-%f")
        file_name = f"{date_time}.html"

        path_file = os.path.join(path, file_name)

        with open(path_file, 'a', encoding="utf-8") as f:
            template = open(path + f'\\{name_template}.html', 'r', encoding="utf-8")
            data_template = template.read()
            f.write(data_template)
            template.close()
            f.close()

        with open(path_file, 'r', encoding="utf-8") as f:
            data_file = f.readlines()
            data_string = json.dumps(data_validations)
            data_string = f"data = {data_string};"
            data_without_spaces = [i.strip() for i in data_file]

            try:
                index = data_without_spaces.index("window.onload = (event) => {")
            except ValueError:
                print("Hubo un error al generar el template de evidencias")

            data_file[index + 1] = data_string
            for line in data_file:
                line = line.strip()
                changes = line.replace('\n', "")
                changes = changes.replace('\\"', '"')
                replacement = replacement + changes
            f.close()

        with open(path_file, 'w', encoding="utf-8") as f:
            f.writelines(replacement)
            f.close()

        return path_file

    @staticmethod
    def attach_json(dict_to_json):

        """
             Description:
                Adjunta la validación del status code en un paso de Allure en formato json.
             Args:
                dict_to_json (dict): Diccionario con información de la validación realizada.
        """

        with allure.step(u"PASO: Se valida el status code esperado"):
            allure.attach(json.dumps(dict_to_json, indent=4), "Validación de status code",
                          attachment_type=allure.attachment_type.JSON)
            unittest.TestCase().assertEqual(dict_to_json['status_code_esperado'], dict_to_json['status_code_obtenido'],
                                            f"El status code no es el esperado, el value obtenido es "
                                            f"{dict_to_json['status_code_obtenido']}")

    def get_random(self, min_range, max_range):

        """
            Description:
                Obtiene un número aleatorio del rango especificado.
            Args:
                min_range (int): Rango mínimo.
                max_range (int): Rango máximo.
            Returns:
                Retorna un número aleatorio.
        """

        return GenericFunctions.get_random(self, min_range, max_range)

    @staticmethod
    def get_random_string(numbers_characters):

        """
            Description:
                Genera una palabra random.
            Args:
                numbers_characters: Recibe la cantidad de caracteres que debe contener el value_text a generar.
            Returns:
                Devuelve un value_text random.
        """

        value = ""
        letters = string.ascii_letters
        for i in range(int(numbers_characters)):
            value_partial = str(random.choice(letters))
            value = f"{value}{value_partial}"

        return value

    @staticmethod
    def get_random_by_date(type_value="value_text"):

        """
            Description:
                Genera un value a partir de la fecha que puede ser integer o value_text.
            Args:
                type_value: El tipo de value que se desea recibir.
            Returns:
                Devuelve un integer con la variable generada apartir de la fecha.
                Devuelve un string con la variable generada apartir de la fecha.
        """

        if type_value == "value_text":
            return str(time.strftime("%d%m%Y%H%M%S"))
        if type_value == "integer":
            return int(time.strftime("%d%m%Y%H%M%S"))

    @staticmethod
    def get_random_list_unique(min_range, max_range, number_results):

        """
            Description:
                Obtiene números aleatorios de una lista del ranngo especificado.
            Args:
                min_range (int): Rango mínimo.
                max_range (int): Rango máximo.
                number_results (int): Cantidad de números a obtener.
            Returns:
                Retorna números aleatorios.
        """

        return random.sample(range(min_range, max_range), number_results)

    # BASE DE DATOS ####################################################################################################
    def set_timeout_base_sql_server(self, time_seconds):

        """
            Description:
                Configura el value de timeout (segundos) configurado para las conexiones a bases sqlServer.
            Args:
                time_seconds: Valor (int) que representa una cantidad en segundos.
        """

        GenericFunctions.set_timeout_base_sql_server(self, time_seconds)

    def get_timeout_base_sql_server(self):

        """
            Description:
                Devuelve el value de timeout configurado para la conexion a bases sqlServer.
            Return:
                Devuelve el value de timeout (segundos) configurado para la conexion a bases sqlServer.
        """

        return GenericFunctions.get_timeout_base_sql_server(self)

    def establish_connection_sqlserver(self, server, base, user, password):

        """
            Description:
                Realiza conexión a una base de datos sqlServer.
            Args:
                server: Servidor ip
                base: nombre de la base
                user: usuario
                password: Contraseña
            Return:
                Devuelve una variable con la conexion a la base de datos sqlServer.
        """

        return GenericFunctions.establish_connection_sqlserver(self, server, base, user, password)

    def check_base_sqlserver(self, server, base, user, password, query):

        """
            Description:
                Realiza conexión y consulta a base de datos con la libreria pyodbc. El metodo incluye la
                desconexión.
            Args:
                server: Servidor ip.
                base: Nombre de la base.
                user: Usuario.
                password: Contraseña.
                query: Consulta Query.
            Returns:
                <class 'pyodbc.Row'>: Retorna un class 'pyodbc.Row' si la consulta y la conexión es exitosa. De lo
                contrario imprime por consola "Se produjo un error en la base de datos."
        """

        return GenericFunctions.check_base_sqlserver(self, server, base, user, password, query)

    def execute_sp_base_sqlserver(self, server, base, user, password, query, parameters: tuple):

        """
            Description:
                Realiza conexión y consulta a base de datos con la libreria pyodbc. El metodo incluye la
                desconexión.
            Args:
                server (str): Servidor ip.
                base (str): Nombre de la base.
                user (str): Usuario.
                password (str): Contraseña.
                query (str): Consulta Query.
                parameters (tuple): Tupla con parametros para el sp.
            Returns:
                Lista con los resultados.
        """

        return GenericFunctions.execute_sp_base_sqlserver(self, server, base, user, password, query, parameters)

    def get_list_base_sqlserver(self, server, base, user, password, query):

        """
            Description:
                Realiza conexión y consulta a base de datos con la libreria pyodbc. El metodo incluye la
                desconexión.
            Args:
                server (str): Servidor ip.
                base (str): Nombre de la base.
                user (str): Usuario.
                password (str): Contraseña.
                query (str): Consulta Query.
            Returns:
                Lista con los resultados.
        """

        return GenericFunctions.get_list_base_sqlserver(self, server, base, user, password, query)

    def delete_reg_base_sqlserver(self, server, base, user, password, query):

        """
            Description:
                Elimina un registro de la base de datos. El método incluye la desconexión.
            Args:
                server: Servidor ip.
                base: Nombre de la base.
                user: Usuario.
                password: Contraseña.
                query: Consulta Query.
            Returns:
                Imprime por consola "Ocurrió un error en la base".
        """

        GenericFunctions.delete_reg_base_sqlserver(self, server, base, user, password, query)

    @staticmethod
    def check_base_oracle(server, base, encoding, user, password, query):

        """
            Description:
                Realiza la conexión y consulta a base de datos Oracle. El método incluye la desconexión.
            Args:
                server: Servidor ip.
                base: Nombre de la base.
                encoding: Tipo de codificación de la base.
                user: Usuario.
                password: Contraseña.
                query: Consulta Query.
            Returns:
                <class 'cx_Oracle.Row'>: Retorna un class 'cx_Oracle.Row' si la consulta y la conexión es exitosa. De lo
                contrario imprime el error por consola.
        """

        record = ""
        connection = None
        dsn = server + '/' + base
        try:
            connection = cx_Oracle.connect(user, password, dsn, encoding=encoding)
            cursor = connection.cursor()
            cursor.execute(query)
            for row in cursor:
                record = row
            return record

        except cx_Oracle.Error as error:
            print(error)

        finally:
            if connection:
                connection.close()

    # FUNCIONES DE TIEMPO ##############################################################################################
    @staticmethod
    def get_date():

        """
            Description:
                Obtiene la fecha del sistema.
            Returns:
                Retorna fecha del sistema.
        """

        dia_global = time.strftime(Parameters.date_format)  # formato dd/mm/aaaa
        print(f'Fecha del sistema {dia_global}')
        return Functions.global_date

    @staticmethod
    def get_time():

        """
            Description:
                Obtiene la hora del sistema.
            Returns:
                Retorna la hora del sistema.
        """

        hora_global = time.strftime(Parameters.time_format)  # formato 24 houras
        print(f'Hora del sistema {hora_global}')
        return Functions.global_time

    @staticmethod
    def get_date_time():

        """
            Description:
                Obtiene la fecha y hora del sistema.
            Returns:
                Retorna fecha y la hora del sistema.
        """

        global_date = time.strftime(Parameters.date_format)  # formato dd/mm/aaaa
        global_time = time.strftime(Parameters.time_format)  # formato 24 houras
        date_time = f'{global_date} {global_time}'
        print(f"La fecha y hora del sistema es: {date_time}")
        return date_time

    @staticmethod
    def get_difference_datetime(datetime_one, datetime_two):

        """
            Description:
                Calcula la diferencia entre dos fechas.
            Args:
                datetime_one: Fecha.
                datetime_two: Fecha.
            Returns:
                Retorna la diferencia entre dos fechas.
        """

        format_date = Parameters.date_format + " " + Parameters.time_format
        datetime_one = datetime.datetime.strptime(datetime_one, format_date)
        datetime_two = datetime.datetime.strptime(datetime_two, format_date)
        difference = datetime_one - datetime_two
        print(f"Diferencia de fechas: {difference}")
        return difference

    @staticmethod
    def convert_bits_to_date(date_bit):

        """
            Description:
                Convierte una fecha de formato BIT a una fecha en formato DATE.
            Args:
                date_bit: Recibe una fecha en formato Bit.
            Returns:
                Devuelve una fecha en formato date.
        """

        timestamp_with_ms = date_bit
        timestamp, ms = divmod(timestamp_with_ms, 1000)
        dt = datetime.datetime.fromtimestamp(timestamp) + datetime.timedelta(milliseconds=ms)
        formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_time

    @staticmethod
    def add_delta_hours_to_datetime(add_time_delta: tuple):

        """
            Description:
                Suma un tiempo delta definido en horas, minutos y segundos a la fecha y hora actual.
            Args:
                add_time_delta: tupla con el tiempo (horas, minutos, segundos) que desea ser agregado.
            Return:
                Devuelve la fecha actual con el tiempo adicional.
        """

        add_time = datetime.timedelta(hours=add_time_delta[0], minutes=add_time_delta[1], seconds=add_time_delta[2])
        now = datetime.datetime.now()
        new_datetime = now + add_time
        date_time_format = f"{Parameters.date_format} {Parameters.time_format}"
        new_datetime = new_datetime.strftime(date_time_format)
        return new_datetime

    @staticmethod
    def hour_rounder(date_time: str):

        """
            Description:
                Redondea la hora de la fecha actual.
            Args:
                date_time: Recibe una fecha en formato value_text con formato "%H:%M:%S %d/%m/%Y"
            Return:
                Devuelve la fecha redondeada.
        """

        date_time_format = f"{Parameters.date_format} {Parameters.time_format}"
        date_time = datetime.datetime.strptime(date_time, date_time_format)
        return (date_time.replace(second=0, microsecond=0, minute=0, hour=date_time.hour) +
                datetime.timedelta(hours=date_time.minute // 30))

    @staticmethod
    def convert_date_to_bit(date_target):

        """
            Description:
                Convierte una fecha de formato date a una fecha en formato BIT.
            Args:
                date_target: Recibe una fecha en formato date.
            Returns:
                Devuelve una fecha en formato bit de 13 digitos.
        """

        unixtime = int(datetime.datetime.timestamp(date_target) * 1000)
        return unixtime

    # FUNCIONES INFORMES ###############################################################################################
    def send_mail(self, receiver_email: list, title, content, file_attach=None):

        """
            Description:
                Envía un informe vía email.
            Args:
                receiver_email (str): Destinatarios del correo.
                title (str): Asunto del correo.
                content (str): Cuerpo del correo.
                file_attach (file): Archivos adjuntos del correo.
            Returns:
                Si el correo fue enviado con éxito retorna el estado "Enviado",
                de lo contrario imprime por consola "El mail no pudo ser enviado" y estado "No enviado".
        """

        return GenericFunctions.send_mail(self, receiver_email, title, content, file_attach=file_attach)

    def create_title(self, title_text: str):

        """
            Descripcion:
                Crea un título en formato html.
            Args:
                title_text: Título en formato value_text.
            Return:
                Devuelve título en formato html.
        """

        return GenericFunctions.create_title(title_text)

    @staticmethod
    def create_message_html(message_text: str, special_strings=None):

        """
            Descripcion:
                Crea un párrafo en formato html.
            Args:
                message_text: párrafo en formato value_text.
                special_strings: Lista de palabras que deben ser resaltadas en negrita dentro del mensaje.
            Return:
                Devuelve párrafo en formato html.
        """

        if special_strings is None:
            special_strings = []
        return GenericFunctions.create_message_html(message_text, special_strings)

    def create_table(self, list_data_head: list, list_data_content: list):

        """
            Descripcion: crea una tabla html.
            Args:
                list_data_head: Lista con los encabezados de la tabla.
                list_data_content: Matriz (lista con lista) con los datos de la tabla.
            Return:
                Devuelve una tabla en formato html.
        """

        return GenericFunctions.create_table(list_data_head, list_data_content)

    def create_style_html(self):

        """
            Description:
                Devuelve el código css con los estilos que deben aplicarse a un bloque HTML.
            Return:
                Devuelve el estilo para aplicar al código html.
        """

        return GenericFunctions.create_style_html()

    def apply_style_css_to_block(self, block_html: str):

        """
            Description:
                Aplica estilos css a un bloque html.
            Args:
                block_html: Bloque html que recibirá los estilos css.
            Return:
                Devuelve un bloque html con estilos aplicados.
        """

        return GenericFunctions.apply_style_css_to_block(block_html)

    @staticmethod
    def print_precondition_data(precondition_json):

        """
            Description:
                Adjunta en el reporte de allura un json con los datos pre condición utilizados en la prueba.
            Args:
                precondition_json (str): Datos pre condición en formato json.
        """

        with allure.step(u"PASO: Se utilizan lo siguientes datos como pre condición"):
            allure.attach(json.dumps(precondition_json, indent=4),
                          "Datos pre condición",
                          attachment_type=allure.attachment_type.JSON)

    def set_new_value_json(self, json_data, claves,  valor_nuevo=None):
        '''
            Modifica el value de una key o elimina key/value del json, segun el tipo_accion.
            En caso de no encontrar lanza un mensaje de error
            :param json_data: contiene dict_to_json del json original
            :param valor_nuevo:(opc) nuevo value que se toma para el caso de modificar del json
            :return: json modificado con el nuevo value
        '''

        if (str(type(claves)) != "<class 'list'>"):
            claves = claves.split('.')

        if len(claves) == 1:
            if str(type(json_data)) != "<class 'list'>":
                self.assertIn(claves[0], json_data, "No se encontro la clave")
            if (str(type(json_data)) == "<class 'list'>"):
                json_data[0][claves[0]] = valor_nuevo
            else:
                json_data[claves[0]] = valor_nuevo
            return json_data

        elif len(claves) == 2:
            if str(type(json_data)) != "<class 'list'>":
                self.assertIn(claves[0], json_data, "No se encontro la clave")
            if (str(type(json_data)) == "<class 'list'>"):
                json_data[0][claves[0]][0][claves[1]] = valor_nuevo
                return json_data

        self.set_new_value_json(json_data[claves.pop(0)], claves,  valor_nuevo)
        return json_data

    def delete_value_json(self, json_data, claves):
        '''
            Modifica el value de una key o elimina key/value del json, segun el tipo_accion.
            En caso de no encontrar lanza un mensaje de error
            :param tipo_accion: determina la accion a realizar. Valores posibles 'MODIFICA' o 'ELIMINA'
            :param json_data: contiene dict_to_json del json original
            :param valor_nuevo:(opc) nuevo value que se toma para el caso de modificar del json
            :return: json modificado con el nuevo value
        '''

        if(str(type(claves)) != "<class 'list'>"):
            claves = claves.split('.')

        if len(claves) == 1:
            if str(type(json_data)) != "<class 'list'>":
                self.assertIn(claves[0], json_data, "No se encontro la clave")
                if (str(type(json_data)) == "<class 'list'>"):
                    del json_data[0][claves[0]]
                else:
                    del json_data[claves[0]]

            return json_data

        elif len(claves) == 2:
            if str(type(json_data)) != "<class 'list'>":
                self.assertIn(claves[0], json_data, "No se encontro la clave")
                if (str(type(json_data)) == "<class 'list'>"):
                    del json_data[0][claves[0]][0][claves[1]]
                    return json_data

        self.delete_value_json(json_data[claves.pop(0)], claves)
        return json_data
    ####################################### Jira conections ############################################################

    def write_cell(self, cell, value, name, folder='files', sheet=None):

        """
            Description:
                Permite escribir en una celda indicada de una hoja especifica para un
                libro de excel en directorio ./inputs/.
            Args:
                cell (obj): Celda de la hoja, se espera COLUMNA+FILA.
                value (str): Valor a ingresar en la celda.
                name (str): Nombre del libro de excel, en el directorio ./inputs/.
                sheet (str): Hoja especifica del libro excel.
                folder (str): Nombre de la carpeta que contiene el libro excel. Es 'files' por default o puede ser
                'downloads'.
            Returns:
                Imprime por consola la celda, hoja y valor escrito, y devuelve TRUE
                en caso contrario imprime por consola "VERIFICAR: No se pudo escribir el archivo."
                y devuelve FALSE.
        """
        return GenericFunctions.write_cell(self, cell, value, name, folder, sheet)

