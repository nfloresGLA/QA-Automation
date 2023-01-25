# -*- coding: utf-8 -*-
import ctypes
import pyperclip3
import allure
from functions.Parameters import Parameters
from functions.Functions import Functions as FunctionsGeneric
import os
import lackey
from lackey import Location, Mouse
import win32com.client as wshshell
import unittest
import json
import time
import pprint
import easyocr
import base64
from PIL import ImageGrab
import numpy as np
import cv2
from pynput.keyboard import Controller


class Functions(FunctionsGeneric, Parameters):
    my_app = None
    data_objects = {}
    my_screen = None
    menssage = None
    json_strings = None
    json_ValueToFind = None
    json_GetFieldBy = None

    def set_proyect(self, project_name=None):

        """

            Description:
                Setea variables de ambiente y rutas del proyecto.

            Args:
                project_name (str): Nombre del Proyecto

            Returns:
                Imprime por consola la siguiente configuración:
                    -Ambiente.
                    -Ruta de Resource.
                    -Ruta de Evidencias.
                    -Ruta de los Json.
                    -Ruta de las Imagenes de los json (reconocimiento por imagenes).
                    -Ruta de los Bass.

                Si hubo un error en la configuración, imprime por consola
                "No se pudieron detectar los datos de la ejecución".

        """
        Functions.show_window_size()
        FunctionsGeneric.set_proyect(self, project_name)

    def set_retry(self, numbers_retries):

        """

            Description:
                Configura la cantidad de reintentos que se realizan al buscar algun objeto o realizar alguna espera.

            Args:
                numbers_retries: Número entero que se utilizará como nuevo parametro para la búsqueda de objetos.

        """

        FunctionsGeneric.set_retry(self, numbers_retries)

    def set_screen(self, number_screen=0):

        """

            Description:
                Setea en cuál monitor se mostrará la pantalla. El monitor principal es 0.

            Args:
                number_screen: Número entero que indica en cúal monitor se verá la pantalla.

        """

        self.my_screen = lackey.Screen(number_screen)
        self.data_objects["APLICACIONES"] = [{"OBJETOS": {}}]

    def open_app(self, application, screen=0):

        """

            Description:
                Abre la app.

            Args:
                application: Nombre de la app que se abrirá.
                screen: Número entero que indica en cúal monitor se verá la pantalla.

        """

        lackey.Settings.MoveMouseDelay = 0.0
        lackey.Settings.InfoLogs = False
        lackey.Settings.ActionLogs = False
        self.my_screen = lackey.Screen(screen)
        self.data_cache["PATH APLICACION"] = application.replace(application.split("\\")[-1], "")
        self.data_cache["APLICACION"] = application.split("\\")[-1]
        os.startfile(application)
        print(f"Abriendo aplicación '{self.data_cache['APLICACION']}'")
        self.data_objects["APLICACIONES"] = [{"NOMBRE DE APLICACION": self.data_cache['APLICACION'], "OBJETOS": {}}]

    def highlight_active_app(self, color="green"):

        """

            Description:
                Señala la aplicación que se encuentre activa en primer plano.

            Args:
                color = Es el color con el que se produce el señalamiento(por default en verde).

        """

        for x in range(1):
            self.my_app.focusedWindow().highlight(True, 1, color)
            time.sleep(0.1)

    def close_app(self, app=None):

        """

            Description:
                Cierra la app. (NO FUNCIONA)

        """

        if app is None:
            if self.data_cache['APLICACION'] != 'CMD.exe':
                os.system(f"Taskkill /IM {self.data_cache['APLICACION']} /F")
            else:
                print("No esta permitido cerrar CMD.EXE")
        else:
            if app != 'CMD.exe':
                os.system(f"Taskkill /IM {app} /F")
            else:
                print("No esta permitido cerrar CMD.EXE")

    def get_element(self, entity):

        """

            Description:
                Gestiona la búsqueda de la entidad en pantalla e instancia un objeto "Element" que permite
                su manipulación.

            Args:
                Entity: Nombre de la entidad buscada.

            Returns:
                Objecto 'Element' con el que se pueden realizar acciones que utilizan los dispositivos simulados.

        """

        if entity is not None:
            Functions.get_entity(self, entity)
            element = Functions.capture_element(self, entity)
        else:
            element = None

        class Element:
            message = None

            def __init__(self, instance, element_context, entity_context):
                self.instance = instance
                self.element = element_context
                self.entity = entity_context

            def click(self):

                """

                    Description:
                        Ejecuta acción click.

                """

                self.execute_action("click")

            def double_click(self):

                """

                    Description:
                        Ejecuta acción doble click.

                """

                self.execute_action("double_click")

            def send_keys(self, value):

                """

                    Description:
                        Escribe sobre un campo.

                    Args:
                        value: Toma como valor un texto.

                """

                self.execute_action("send_keys", value)

            def send_keys_ascii(self, value):

                """

                    Description:
                        Escribe un caracter especial utilizando su código ascii.

                    Args:
                        value: Toma como valor un código ascii.

                """

                self.execute_action("send_keys_ascii", value)

            def press_keys(self, value):

                """

                    Description:
                        Escribe sobre la aplicación activa en primer plano.

                    Args:
                        value: Toma como valor un texto.

                """

                self.execute_action("press_keys", value)

            def send_special_key(self, value):

                """

                    Description:
                        Presiona teclas especificas sobre la aplicación activa en primer plano.

                    Args:
                        value: Toma como valor una tecla especial(EJ: 'ENTER', 'TAB').

                """

                self.execute_action("send_special_key", value)

            def send_symbol(self, value):

                """

                    Description:
                        Presiona teclas específicas sobre la aplicación activa en primer plano.

                    Args:
                        value: Toma como valor un símbolo.

                """

                self.execute_action("send_symbol", value)

            def is_displayed(self):

                """

                    Description:
                        Consulta si se encuentra el objeto en pantalla.

                    Returns:
                        Devuelve True en caso de haber un match del objeto, caso contrario
                        devuelve False.

                """

                return self.execute_action("is_displayed")

            def get_text(self):

                """

                    Description:
                        Obtiene el texto de un campo. (NO DISPONIBLE)

                    Returns:
                        Devuelve el un value_text con el texto obtenido.

                """

                return self.execute_action("get_text")

            def clipboard_value(self, value):

                """

                    Description:
                        Copia el value de una variable dentro del portapapeles de Windows.

                    Args:
                        value: Toma como valor de la variable.

                """

                return self.execute_action("clipboard_value", value)

            def mouse_move(self, value):

                """

                    Description:
                        Mueve el mouse a una locación determinada.

                    Args:
                        value: Toma un número entero como valor.

                """

                return self.execute_action("move_mouse", value)

            def execute_action(self, action, value=None):

                """

                    Description:
                        Ejecuta un conjunto de acciones que pueden requerir o no valores de configuración.

                    Args:
                        value: Parámetro que toma como valor dependiendo de la función que lo llamó.

                """

                try:
                    return self.select_action(action, value)
                except Exception as e:
                    Functions.screenshot("Ultima screenshot antes de finalizar la ejecución")
                    self.instance.fail(e.__class__.__name__)

            def select_action(self, action, value=None):

                if action == "move_mouse":
                    loc = Location(x=value[0], y=value[1])
                    lackey.Mouse.move(Mouse(), loc=loc)

                if action == "click":
                    self.message = f"Se realizará click en el objeto {entity}"
                    lackey.Region.click(element)


                elif action == "double_click":
                    self.message = f"Se realizará doble click en el objeto {entity}"
                    lackey.Region.doubleClick(element)

                elif action == "click_right":
                    self.message = f"Se realizará click derechi en el objeto {entity}"
                    lackey.Region.rightClick(element)

                elif action == "send_keys":
                    self.message = f"Se escribirá en el campo {entity}"
                    lackey.Region.click(element)
                    wshshell.Dispatch("WScript.Shell").SendKeys(value)

                elif action == "send_keys_ascii":
                    #falta finalizar
                    self.message = "escribir caracter especial"

                elif action == "clipboard_value":
                    self.message = f"{value} se encuentra disponible para su uso (pegado)"
                    pyperclip3.copy(value)

                elif action == "is_displayed":
                    self.message = f"Se ha encontrado el objeto buscado '{self.entity}'."
                    if self.element.__class__.__name__ == 'Match':  # Pregunta si encontro una coincidencia
                        return True
                    else:
                        return False

                elif action == "send_keys_legacy":
                    self.message = "escribir en el campo"
                    lackey.Region.click(element)
                    lackey.Keyboard().type(value)

                elif action == "press_keys":
                    self.message = f"Se escribirá el texto {value} en el objeto {entity}"
                    wshshell.Dispatch("WScript.Shell").SendKeys(value)

                elif action == "send_symbol":
                    self.message = f"Se escribirá el simbolo {value} en el objeto {entity}"
                    pynput_symbol = Controller()
                    pynput_symbol.press(value)

                elif action == "send_special_key":
                    self.message = f"Se presionará la tecla {value}"
                    key = value.upper()
                    if key == 'ENTER':
                        lackey.Keyboard().type(lackey.Key.ENTER)
                    if key == 'TAB':
                        lackey.Keyboard().type(lackey.Key.TAB)
                    if key == 'ESPACIO':
                        lackey.Keyboard().type(lackey.Key.SPACE)
                    if key == 'ESCAPE':
                        lackey.Keyboard().type(lackey.Key.ESC)
                    if key == 'RETROCESO':
                        lackey.Keyboard().type(lackey.Key.BACKSPACE)
                    if key == 'SUPRIMIR':
                        lackey.Keyboard().type(lackey.Key.DELETE)
                    if key == "ABAJO":
                        lackey.Keyboard().type(lackey.Key.PAGE_DOWN)
                    if key == "ARRIBA":
                        lackey.Keyboard().type(lackey.Key.PAGE_UP)
                    if key == "DERECHA":
                        lackey.Keyboard().type(lackey.Key.RIGHT)
                    if key == "CONTROL+TAB":
                        lackey.Keyboard().keyDown('{CTRL} {TAB}')
                        lackey.Keyboard().keyUp('{CTRL} {TAB}')
                    if key == "WINDOWS":
                        lackey.Keyboard().type(lackey.Key.WIN)

                elif action == "get_text":
                    result = None
                    get_text_list = []
                    self.message = f"Se obtendrá el texto ubicado en el objeto {entity}"
                    if self.element is None:
                        if entity in self.instance.data_objects["APLICACIONES"][0]["OBJETOS"]:
                            image = self.instance.my_screen.capture(
                                self.instance.data_objects["APLICACIONES"][0]["OBJETOS"][entity])
                            reader = easyocr.Reader(["es"], gpu=False)
                            result = reader.readtext(image)
                        else:
                            print("No se encontro el objeto buscado en cache.")
                            get_text_list = None
                    else:
                        image = self.instance.my_screen.capture(self.element.getTuple())
                        reader = easyocr.Reader(["es"], gpu=False)
                        result = reader.readtext(image)
                    for inner_elements in result:
                        get_text_list.append(inner_elements[1])
                    return get_text_list
                print(f" -> {self.message}")


        return Element(self, element, entity)

    def capture_element(self, entity):

        """

            Description:
                Realiza la búsqueda de un objeto en pantalla. Si encuentra coincidencias carga el objeto en memoria y
                devuelve su localización.

            Args:
                entity: Es el nombre del objeto que se desea encontrar.

            Returns:
                La localizacion del objeto en pantalla

        """

        for intentos in range(Parameters.number_retries):
            try:
                element_path = f"{self.path_images}\\{self.json_ValueToFind}"
                element_location = self.my_screen.find(element_path)
                if element_location:
                    if entity not in self.data_objects["APLICACIONES"][0]["OBJETOS"]:
                        self.data_objects["APLICACIONES"][0]["OBJETOS"].update({entity: element_location.getTuple()})
                    else:
                        print(f"El objeto {entity} ya existe en cache y no se actualizaran sus coordenadas.")
                    return element_location
            except lackey.Exceptions.FindFailed:
                Functions.wait(self, Parameters.time_between_retries, f"Esperando a {entity}")
            except Exception as e:
                print(e)
                Functions.wait(self, Parameters.time_between_retries, f"Esperando a {entity}")
        return None

    @staticmethod
    def screenshot(description):
        img = ImageGrab.grab()
        img_np = np.array(img)
        frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        _, imagebytes = cv2.imencode('.png', frame)
        img_b64 = base64.b64encode(imagebytes)
        allure.attach(base64.decodebytes(img_b64), description, attachment_type=allure.attachment_type.PNG)

    def wait(self, seconds, logger=Parameters.loggin_time, reason=None):

        """

            Description:
                Inicia una espera.

            Args:
                seconds: Tiempo de espera establecido en segundos.
                logger:
                reason: Motivo de la espera.

        """

        FunctionsGeneric.wait(self, seconds, logger, reason=reason)

    def get_entity(self, entity):

        """

            Description:
                Lee una entidad del archivo json.

            Args:
                entity (str): Nombre de la entidad que se quiere buscar.

            Returns:
                Si la entidad fue encontrada retorna "True", en caso contrario imprime
                "get_entity: No se encontro la key a la cual se hace referencia: " + entity".

        """

        if self.json_strings is False:
            unittest.TestCase().skipTest("EL repositorio de objetos no ha sido definido.")
        else:
            try:
                self.json_ValueToFind = self.json_strings[entity]["ValueToFind"]
                self.json_GetFieldBy = self.json_strings[entity]["GetFieldBy"]

            except KeyError:
                unittest.TestCase().skipTest(f"--KeyErrorException-- No se encontro la key a la cual se hace "
                                             f"referencia: {entity}")
                Functions.tear_down(self)

    def get_json_file(self, file):

        """

            Description:
                Lee un archivo json.

            Args:
                file (file): Archivo json

            Returns:
                Si el archivo fue encontrado imprime "get_json_file: " + json_path",
                en caso contrario imprime "get_json_file: No se encontro el Archivo " + file".

        """

        json_path = f"{self.path_json}\\{file}.json"
        try:
            with open(json_path, "r", encoding='utf8') as read_file:
                self.json_strings = json.loads(read_file.read())

        except FileNotFoundError:
            unittest.TestCase().skipTest(f"--NoFoundJsonFileException-- No se encontro el Archivo {file}")
            Functions.tear_down(self)

    def print_data_object(self):

        """
            Description:
                Imprime en pantalla los objectos encontrados.

        """

        pprint.pprint(self.data_objects["APLICACIONES"])

    def tear_down(self):

        """

            Description:
               Cierra la aplicación y finaliza el proceso.
               Cierra la aplicación que se encuentra en Foco (instancia base).

        """

        pprint.pprint(self.data_objects["APLICACIONES"][0]["OBJETOS"])
        Functions.close_app(self)

    def send_mail(self, receiver_email: list, title, content, file_attach=None):

        """
        
            Description:
                Envia un informe vía email.

            Args:
                receiver_email (str): Destinatarios del correo.
                title (str): Asunto del correo.
                content (str): Cuerpo del correo.
                file_attach (file): Archivos adjuntos del correo.

            Returns:
                Si el correo fue enviado con éxito retorna el estado "Enviado",
                de lo contrario imprime por consola "El mail no pudo ser enviado" y estado "No enviado".

        """

        return FunctionsGeneric.send_mail(self, receiver_email, title, content, file_attach=None)

    @staticmethod
    def show_window_size():

        """

             Description:
                Imprime el tamaño actual de la pantalla.

        """

        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        normalized_height = screensize[1]
        normalized_width = screensize[0]
        print(f"Tamaño de pantalla: {normalized_height}x{normalized_width}")

    def get_random(self, min_range, max_range):

        """

            Description:
                Obtiene un número aleatorio del rango especificado.

            Args:
                min_range (int): Rango mínimo
                max_range (int): Rango máximo

            Returns:
                Retorna un número aleatorio.

        """

        random_number = FunctionsGeneric.get_random(self, min_range, max_range)
        return random_number

    def create_title(self, title_text: str):

        """

            Description:
                Crea un título en formato html.

            Args:
                title_text: Título en formato value_text.

            Returns:
                Devuelve título en formato html.

        """

        return FunctionsGeneric.create_title(title_text)

    def create_message_html(self, message_text: str, special_strings=None):

        """

            Description:
                Crea un párrafo en formato html.

            Args:
                message_text: Mensaje en formato string.
                special_strings: Lista de palabras que deben ser resaltadas en negrita dentro del mensaje.

            Returns:
                Devuelve el párrafo en formato html.

        """

        return FunctionsGeneric.create_message_html(message_text, special_strings)

    def create_table(self, list_data_head: list, list_data_content: list):

        """

            Description:
                Crea una tabla html.

            Args:
                list_data_head: Lista con los encabezados de la tabla.
                list_data_content: Matriz (lista con lista) con los datos de la tabla.

            Returns:
                Devuelve una tabla en formato html.

        """

        return FunctionsGeneric.create_table(list_data_head, list_data_content)

    def create_style_html(self):

        """

            Description:
                Devuelve el código css con los estilos que deben aplicarse a un bloque HTML.

            Returns:
                Devuelve el estilo para aplicar al código html.

        """

        return FunctionsGeneric.create_style_html()

    def apply_style_css_to_block(self, block_html: str):

        """

            Description:
                Aplica estilos css a un bloque html.

            Args:
                block_html: Bloque html que recibirá los estilos css.

            Returns:
                Devuelve un bloque html con estilos aplicados.

        """

        return FunctionsGeneric.apply_style_css_to_block(block_html)

    def create_teams_notifications(self, teams_channel=None, table_color=None, msg_tittle=None,
                                   section_text=None, btn_name=None, btn_link=None):

        """

            Description:
                  Genera una notificación de teams en el canal requerido.

            Args:
                teams_channel= WebHook al canal de teams (Obligatorio).
                table_color= Color del thead (Opcional).
                msg_tittle= Título del mensaje (Opcional).
                section_tittle= Título de sección (Opcional).
                section_text= Texto de sección (Opcional).
                btn_name= Nombre de Botón (Opcional).
                btn_link= Link de acción para el botón (Obligatorio).

        """

        FunctionsGeneric.create_teams_notifications(self, teams_channel, table_color, msg_tittle,
                                                    section_text, btn_name, btn_link)

    def write_cell(self, cell, value, name, sheet=None):

        """
            Description:
                Permite escribir en una celda indicada de una hoja especifica para un
                libro de excel en directorio ./inputs/.
            Args:
                cell (obj): Celda de la hoja, se espera COLUMNA+FILA.
                value (str): Valor a ingresar en la celda.
                name (str): Nombre del libro de excel, en el directorio ./inputs/.
                sheet (str): Hoja especifica del libro excel.
            Returns:
                Imprime por consola la celda, hoja y valor escrito, y devuelve TRUE
                en caso contrario imprime por consola "VERIFICAR: No se pudo escribir el archivo."
                y devuelve FALSE.
        """
        return FunctionsGeneric.write_cell(self, cell, value, name, sheet)
