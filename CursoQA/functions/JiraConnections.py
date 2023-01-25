import os
import pprint
import sys
import requests
from requests.auth import HTTPBasicAuth
import json

basedir = os.path.abspath(os.path.join(__file__, "../../../../.."))


class JiraConnections:
    def __init__(self, instancia, user_description, error_code, id_project, report_file, data_cache, data_resource,
                 exception_handling, label_id, token_jira, true_custom_fields):
        self.report_file_img = report_file
        self.user_description = user_description
        self.error_code = error_code
        self.id_project = id_project
        self.data_cache = data_cache
        self.data_resource = data_resource
        self.exception_handling = exception_handling
        self.label_id = label_id
        self.token_jira = token_jira
        self.instancia = instancia
        self.true_custom_fields = true_custom_fields

    def main(self):
        self.report_defect

    @property
    def report_defect(self):
        # Ordenar las keys y values del data resource
        resource_ordenado = ''
        for key in self.data_resource:
            resource_ordenado += ("\n           * {}: {}".format(key, self.data_resource[key]))

        # Ordenar las keys y values del data cache
        cache_ordenado = ''
        for key in self.data_cache:
            cache_ordenado += ("\n           * {}: {}".format(key, self.data_cache[key]))

        # variables para generar la descripción del caso
        ####################################################****************************
        description_header = f"Informer ID: {self.label_id}"
        description_body = f"\n \n " \
                           f"Información Extra suministrada por el usuario: " \
                           f"\n -{self.user_description}" \
                           f"\n" \
                           f"\n -Resultado Esperado: {self.instancia.message_container}" \
                           f"\n" \
                           f"\n -Resultado Obtenido: {self.exception_handling}" \
                           f"\n" \
                           f"\n -Resource info: {resource_ordenado}" \
                           f"\n" \
                           f"\n -Cache info: {cache_ordenado}" \
                           f"\n" \
                           f"\n -Lista de pasos: \n {self.instancia.steps_case}" \
            ####################################################****************************
        summary_text = f'AUTOMATION || {self.error_code}'
        # validacion de bug dentro de jira
        is_already_reported = self.buscar_defectos_proyecto(summary_text)
        if is_already_reported == True:
            # Bug reportado
            print("Ya existe este defecto")
            return 3312
        else:
            print("Iniciando Reporte!")

            print(f"ID: {self.id_project}")
            endpoint = f"https://andreani.atlassian.net//rest/api/2/issue/"
            headers = \
                {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                }
            payload = {
                "fields":
                    {
                        "project":
                            {
                                "key": f"{self.id_project}"
                            },
                        "summary": f'AUTOMATION || {self.error_code}',
                        "description": description_header + description_body,
                        "issuetype": {"name": "Bug"}
                    }
            }
            payload['fields'].update(self.true_custom_fields)
            payload = json.dumps(payload)
            response = requests.post(endpoint, headers=headers, data=payload, auth=(self.label_id, self.token_jira))
            # print(response.text)
            # Separo la key del nuevo defecto creado
            print(response.json())
            new_id_issue = response.json()['key']
            # print(new_id_issue)
            # Luego de crear el defecto se le adjunta la imagen
            dominio_defecto = 'https://andreani.atlassian.net//rest/api/2/issue/' + new_id_issue + "/attachments"
            auth = HTTPBasicAuth(self.label_id, self.token_jira)
            # creo directorio y archivo de imagen
            with open(os.path.join(self.instancia.path_output, "jira_report.png"), "wb") as create_image:
                create_image.write(self.report_file_img)
                create_image.close()
            with open(os.path.join(self.instancia.path_output, "jira_report.png"), "rb") as f_image:
                upload_file = f_image.read()
            headers_defecto = {
                "X-Atlassian-Token": "no-check",
            }
            files = {
                'file': (
                    "evidencia.png", upload_file)
            }
            requests.post(dominio_defecto, headers=headers_defecto, files=files, auth=auth)
            os.remove(os.path.join(self.instancia.path_output, "jira_report.png"))
            f_image.close()

    def buscar_defectos_proyecto(self, summary):
        endpoint = f"https://andreani.atlassian.net/rest/api/2/search"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = {"jql": f"project =  {self.id_project} AND issuetype in ('Bug (subtarea)','Bug')", "startAt": 0,
                   "maxResults": 100,
                   "fields": ["id", "key", "summary", "issuetype", "status", "reporter", "project"]}
        response = requests.post(endpoint, headers=headers, json=payload,
                                 auth=(self.label_id, self.token_jira))
        pprint.pprint(response.json())
        issues = response.json()["issues"]
        # key = None
        for issue in issues:
            if summary == issue["fields"]["summary"]:
                if not issue["fields"]["status"]["name"] in ("Finalizado", "Cancelado"):
                    return True
                else:
                    return False
            else:
                return False


if __name__ == '__main__':
    JiraConnections(sys.argv[1], sys.argv[2], sys.argv[3]).main()
