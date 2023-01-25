# Este archivo manejará los tipos de conexione disponobles en el framework
# siendo estas en inicio:
# conexiones a bases de datos -> db_connection
# conexiones a Jira -> jira_connection
# conexiones a servicios de mail -> e_connection
# XML tools
import xml.etree.ElementTree as ET
import bz2

from cryptography.fernet import Fernet

from functions.Functions import Functions

PATH_ORIGIN_XML = "C:\\testing-Automation\\functions\\src\\environment_access.xml"


class db_connection():
    def get_user_name(self, server_ip, db_name):
        """
            Description:
               Obtiene el nombre de usuario utilizando la ip del server y el nombre de la dbsabia  desde el archivo encriptado.
            Args:
               server_name: Servidor ip.
               db_name: Nombre de la base.
            Returns:
               Retorna user_name
        """
        user_name = None
        xml_file = XmlEcryptedFile.obtain_xml_data(self)
        try:
            for element in xml_file.findall(f"./CLAVES/IP[.='{server_ip}']/../BASE[.='{db_name}']/../USER"):
                if element.text is not None or element.text != "" or element.text != " ":
                    user_name = element.text
        except AttributeError:
            raise AttributeError(f"Ocurrió un error en el tiempo de ejecución, Error Code -> 35")
        except KeyError:
            raise KeyError(f"La key que se intenta buscar no pudo ser encontrada")
        return user_name

    def get_server_ip(self, db_name, user_name):
        """
            Description:
               Obtiene la ip del server utilizando el nombre de la data base y el nombre de usuario
               desde el archivo encriptado.
            Args:
               db_name: Nombre de la base.
               user_name: Nombre de usuario para ingresar a la Data Base.
            Returns:
               Retorna db_server_ip
        """
        db_server_ip = None
        xml_file = XmlEcryptedFile.obtain_xml_data(self)
        try:
            for element in xml_file.findall(f"./CLAVES/BASE[.='{db_name}']/../USER[.='{user_name}']/../IP"):
                if element.text is not None or element.text != "" or element.text != " ":
                    db_server_ip = element.text
        except AttributeError:
            raise AttributeError(f"Ocurrió un error en el tiempo de ejecución, Error Code -> 57")
        except KeyError:
            raise KeyError(f"La key que se intenta buscar no pudo ser encontrada")
        return db_server_ip

    def get_db_name(self, server_ip, user_name):
        """
            Description:
               Obtiene el nombre de la data base utilizando el ip del server y el nombre de usuario
               desde el archivo encriptado.
            Args:
               server_ip: Servidor ip.
               user_name: Nombre de usuario para ingresar a la Data Base.
            Returns:
               Retorna db_name
        """
        db_name = None
        xml_file = XmlEcryptedFile.obtain_xml_data(self)
        try:
            for element in xml_file.findall(f"./CLAVES/IP[.='{server_ip}']/../USER[.='{user_name}']/../BASE"):
                if element.text is not None or element.text != "" or element.text != " ":
                    db_name = element.text
        except AttributeError:
            raise AttributeError(f"Ocurrió un error en el tiempo de ejecución, Error Code -> 79")
        except KeyError:
            raise KeyError(f"La key que se intenta buscar no pudo ser encontrada")
        return db_name

    # Obtiene la password de la conexión a la db deseada
    def get_server_password(self, server_ip, user_name):
        """
             Description:
                Obtiene la contraseña utilizando la dirección del server y el nombre de usuario
                desde el archivo encriptado.
             Args:
                server_ip: Servidor ip.
                user_name: Nombre de usuario para ingresar a la Data Base.
             Returns:
                Retorna server_password
        """
        #server_password = None
        xml_file = XmlEcryptedFile.obtain_xml_data(self)
        try:
            for element in xml_file.findall(f"./CLAVES/IP[.='{server_ip}']/../USER[.='{user_name}']/../PASS"):
                if element.text is not None or element.text != "" or element.text != " ":
                    server_password = element.text
        except AttributeError:
            raise AttributeError(f"Ocurrió un error en el tiempo de ejecución, Error Code -> 103")
        except KeyError:
            raise KeyError(f"La key que se intenta buscar no pudo ser encontrada")
        return server_password

# nuclear proceso de busqueda en XML mediante el xpath en una sola función

class jira_connection():
    def __init__(self, user):
        self.user = user

    def get_token(self):
        """
                Description:
                   Obtiene la contraseña utilizando la dirección del server y el nombre de usuario
                   desde el archivo encriptado.
                Args:
                   server_ip: Servidor ip.
                   user_name: Nombre de usuario para ingresar a la Data Base.
                Returns:
                   Retorna server_password
        """
        user_token = None
        xml_file = XmlEcryptedFile.obtain_xml_data(self)
        try:
            for element in xml_file.findall(f"./TOKEN[@id='{self.user}']/USER_TOKEN"):
                if element.text is not None or element.text != "" or element.text != " ":
                    user_token = element.text
        except AttributeError:
            raise AttributeError(f"Ocurrió un error en el tiempo de ejecución, Error Code -> 103")
        except KeyError:
            raise KeyError(f"La key que se intenta buscar no pudo ser encontrada")
        return user_token


class XmlEcryptedFile:
    def obtain_xml_data(self):
        key = Functions.get_enviroment_key_from_file()
        fe = Fernet(key)
        try:
            with open(PATH_ORIGIN_XML, 'rb') as file:
                data = file.read()
            deencrypted_data = fe.decrypt(data)
            decompressed_data = bz2.decompress(deencrypted_data)
            file.close()
            read_xml_file = ET.fromstring(decompressed_data)
        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo xml, en la ubicación -> {PATH_ORIGIN_XML}")
        return read_xml_file


conection = db_connection().get_server_password("10.20.7.168", "User_Pybot")
conection_jira = jira_connection("fblanco").get_token()
print(conection)
print(conection_jira)

def get_credentials_encrypted(connection: object):
    # todos utilizan el mismo formato para abrir el archivo
    # lo que diferencia la respuesta viene del tipo de conexión y el xpath que voy a utilizar
    if isinstance(connection, db_connection):
        db_password = connection
        if db_password is not None:
            return db_password
        else:
            return "No se encontró la contraseña deseada"
    if isinstance(connection, jira_connection):
        jira_token = connection
        if jira_token is not None:
            return jira_token
        else:
            return "No se encontró la contraseña deseada"


# get_credentials_encrypted(conection_jira)

print(f"PASS: {get_credentials_encrypted(conection)}")
print(f"token: {get_credentials_encrypted(conection_jira)}")
