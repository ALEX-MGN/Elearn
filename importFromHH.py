import requests
import json
import pandas as pd

def makeCSVwithHH():
    "Создаёт csv файл за 21 число со всеми It вакансиями"
    arrayWithName = []
    arrayWithSalaryFrom = []
    arrayWithSalaryTo = []
    arrayWithCurrency = []
    arrayWithAreaName = []
    arrayWithPublishedAt = []

    for hour in range(0,24):
        for page in range(0,21):
            hour = ("0" + str(hour))[-2:]
            hour_from = f"2022-12-21T{hour}:00:00"
            hour_to = f"2022-12-21T{hour}:23:59"
            vacancies = requests.get("https://api.hh.ru/vacancies/", params={"specialization":1, "page":page, "per_page":100, 'date_from':hour_from, 'date_to':hour_to})
            if "items" in json.loads(vacancies.text):
                for vacancy in json.loads(vacancies.text)["items"]:
                    try:
                        arrayWithName.append(vacancy["name"])
                    except:
                        arrayWithName.append("")
                    try:
                        arrayWithSalaryFrom.append(vacancy["salary"]["from"])
                    except:
                        arrayWithSalaryFrom.append("")
                    try:
                        arrayWithSalaryTo.append(vacancy["salary"]["to"])
                    except:
                        arrayWithSalaryTo.append("")
                    try:
                        arrayWithCurrency.append(vacancy["salary"]["currency"])
                    except:
                        arrayWithCurrency.append("")
                    try:
                        arrayWithAreaName.append(vacancy["address"]["city"])
                    except:
                        arrayWithAreaName.append("")
                    try:
                        arrayWithPublishedAt.append(vacancy["published_at"])
                    except:
                        arrayWithPublishedAt.append("")
            else:
                break
            
    table = pd.DataFrame(data = {"name":arrayWithName,"salary_from":arrayWithSalaryFrom,"salary_to":arrayWithSalaryTo,"currency":arrayWithCurrency,"area_name":arrayWithAreaName,"published_at":arrayWithPublishedAt})
    table.to_csv('vacanciesInOneDay.csv', index=False)