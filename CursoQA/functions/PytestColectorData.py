# -*- coding: utf-8 -*-
import pprint
import json
import glob
import sys
import csv
import os

basedir = os.path.abspath(os.path.join(__file__, "../../"))
sys.path.append(basedir)
from functions.Functions import Functions as FunctionsGeneric

TAGS = ["project name", "name", "status", "description", "feature", "story", "tag", "severity", "suite", "autor",
        "subsuite", "host", "thread", "framework", "language", "package", "estimated time", "as_id"]

class PytestColectorData(FunctionsGeneric):

    def __init__(self, project_name, path) -> None:
        if path[-1] != "/":
            path = f"{path}/"
        self.project_name = project_name
        self.path = path

    def main(self):
        list_data_results = self.load_files()
        self.save_csv_results(list_data_results)
        self.call_update_testcase_data(list_data_results)

    def load_files(self):
        list_results = []
        files = glob.glob(f'{self.path}*result.json')
        if len(files) == 0:
            print("No se encontraron archivos de resultados que procesar.")
        else:
            for file in files:
                print(f"El archivo leido es {file}")
                with open(f"{file}", "r", encoding="utf-8") as f:
                    data_results = {}
                    data = json.load(f)
                    labels = data["labels"]
                    data_results["project name"] = self.project_name
                    data_results["name"] = data["name"]
                    data_results["status"] = data["status"]
                    for label in labels:
                        if label["name"].lower() in TAGS:
                            if "value" in label.keys():
                                data_results[label["name"].lower()] = str(label["value"]).lower()
                            else:
                                data_results[label["name"].lower()] = "NULL"
                list_results.append(data_results)
        return list_results

    def save_csv_results(self, list_data_results):
        with open('results compilated.csv', 'w', newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, delimiter="|", fieldnames=TAGS)
            writer.writeheader()
            for results in list_data_results:
                writer.writerow(results)

    def call_update_testcase_data(self, results: list):
        pprint.pprint(results)
        if results != []:
            query_sp = 'EXEC [dbo].[update_testcases_data] @case_name = ?, @project_name = ?, @module = ?, @submodule = ?,' \
                       '@severity = ?, @autor = ?, @tag = ?, @estimated_duration = ?, @id_case = ?'
            for row in results:
                if "as_id" not in row:
                    row['as_id'] = None
                if "severity" not in row:
                    row['severity'] = None
                if "autor" not in row:
                    row['autor'] = None
                if "tag" not in row:
                    row['tag'] = None
                if "estimated time" not in row:
                    row['estimated time'] = 0
                if str(row['estimated time']).isnumeric() is False:
                    row['estimated time'] = 0
                params = (row['name'], row['project name'], row['suite'], row['subsuite'],
                          row['severity'], row['autor'], row['tag'], int(row['estimated time']), row["as_id"])
                FunctionsGeneric.execute_sp_base_sqlserver(self, "10.20.7.168", "Pybot", "User_Pybot", None, query_sp,
                                                           params)
        else:
            print("No existen datos que guardar.")

if __name__ == '__main__':
    len(sys.argv) if len(sys.argv) == 3 else print("Error: Ingresa el nombre del proyecto y la ruta de archivos.")
    PytestColectorData(sys.argv[1], sys.argv[2]).main()
