import csv
import re
import os
import collections.abc
from var_dump import var_dump
from datetime import datetime
from prettytable import PrettyTable

name = input("Введите название файла: ") 
filterVacansie = input("Введите параметр фильтрации: ").split(": ")
sortingParameter = input("Введите параметр сортировки: ")
reverseOrder = input("Обратный порядок сортировки (Да / Нет): ") 
lines = input("Введите диапазон вывода: ").split()
column = input("Введите требуемые столбцы: ").split(", ")
names = []
investment = []

fieldToRus = {
"name":"Название",
"description":"Описание",
"key_skills":"Навыки",
"experience_id":"Опыт работы",
"premium":"Премиум-вакансия",
"employer_name":"Компания",
"currency":"Оклад",
"area_name":"Название региона",
"published_at":"Дата публикации вакансии"
}

fieldToEng = {
"Название": "name",
"Описание":"description",
"Навыки":"key_skills",
"Опыт работы":"experience_id",
"Премиум-вакансия":"premium",
"Компания":"employer_name",
"Оклад": "currency",
"Название региона":"area_name",
"Дата публикации вакансии":"published_at",
"Идентификатор валюты оклада":"currency"
}

fieldWorkExperience = {
"noExperience": "Нет опыта",
"between1And3": "От 1 года до 3 лет",
"between3And6": "От 3 до 6 лет",
"moreThan6": "Более 6 лет"
}

fieldCurrency = {
"AZN": "Манаты",
"BYR": "Белорусские рубли",
"EUR": "Евро",
"GEL": "Грузинский лари",
"KGS": "Киргизский сом",
"KZT": "Тенге",
"RUR": "Рубли",
"UAH": "Гривны",
"USD": "Доллары",
"UZS": "Узбекский сум"
}

currency_to_rub = {  
    "AZN": 35.68,  
    "BYR": 23.91,  
    "EUR": 59.90,  
    "GEL": 21.74,  
    "KGS": 0.76,  
    "KZT": 0.13,  
    "RUR": 1,  
    "UAH": 1.64,  
    "USD": 60.66,  
    "UZS": 0.0055,  
}

class Vacancy:
    def __init__(self, name, description, key_skills, experience_id, premium, employer_name, salary, area_name, published_at):
        self.name = name
        self.description = description 
        self.key_skills= key_skills
        self.experience_id = experience_id
        self.premium = premium 
        self.employer_name= employer_name
        self.salary = salary
        self.area_name = area_name 
        self.published_at = published_at
        self.elements=[name,description,key_skills,experience_id,premium,employer_name,salary,area_name,published_at]
        
class Salary:
    def __init__(self, salary_from, salary_to, salary_gross, salary_currency):
        self.salary_from = salary_from 
        self.salary_to = salary_to
        self.salary_gross = salary_gross
        self.salary_currency = salary_currency 
        self.salary = str('{:,}'.format(int(float(salary_from))).replace(',', ' ')) + " - " + str('{:,}'.format(int(float(salary_to))).replace(',', ' ')) + " (" + fieldCurrency[salary_currency] + ") (" + ("Без вычета налогов" if salary_gross.upper() == "ДА" else "С вычетом налогов") + ")"

class DataSet:
    def __init__(self):
        self.file_name = name
        self.vacancies_objects = []
    
    def readystr(str_value):
        return ' '.join(re.sub(r"<[^>]+>", '', str_value).split())

    def сsv_reader(ﬁle_name): 
        global names
        with open(ﬁle_name, encoding="UTF-8-sig") as File:
            reader = csv.reader(File, delimiter=',')
            for row in reader:
                if(len(names) == 0):
                    names = row
                elif(len(names) == len(row) and not("" in row)):
                    investment.append(row)
        return investment, names


    def csv_ﬁler(self, reader, list_naming):
        for element in reader:
            salary = ["", "", "", ""]
            array = ["","","","","","","","",""]
            namesIndex = ["name", "description", "key_skills", "experience_id", "premium", "employer_name", "salary", "area_name", "published_at"]
            for item in range(len(names)):
                value = element[item]
                value = value.split("\n") if ("\n" in value) else [value]
                arrayWithoutTegs = []
                for word in value:
                    if(word.upper() == "TRUE"):
                        arrayWithoutTegs.append("Да")
                    elif(word.upper() == "FALSE"):
                        arrayWithoutTegs.append("Нет")
                    elif(word in fieldWorkExperience.keys()):
                        arrayWithoutTegs.append(fieldWorkExperience[word])
                    else:
                        arrayWithoutTegs.append(DataSet.readystr(word))
                if(len(arrayWithoutTegs) == 1):
                    arrayWithoutTegs = arrayWithoutTegs[0]
                if(list_naming[item] == "salary_from"):
                    salary[0] = arrayWithoutTegs
                elif(list_naming[item] == "salary_to"):
                    salary[1] = arrayWithoutTegs
                elif(list_naming[item] == "salary_gross"):
                    salary[2] = arrayWithoutTegs
                elif(list_naming[item] == "salary_currency"):
                    salary[3] = arrayWithoutTegs
                    readySalary = Salary(*salary)
                    array[6] = readySalary
                else:
                    array[namesIndex.index(list_naming[item])] = arrayWithoutTegs
            vacancy = Vacancy(*array)
            self.vacancies_objects.append(vacancy)
        return self.vacancies_objects


class InputConnect:
    def __init__(self):
        self.data = DataSet()

    def filterVacancies(self, vacancy):
        if(filterVacansie[0] != ""):
            article = fieldToEng[filterVacansie[0]]
            information = filterVacansie[1]
            if(article == "key_skills" and set(str(information).split(", ")).issubset(set(vacancy.key_skills))):
                return vacancy
            if(article == "currency" and "Идентификатор" not in filterVacansie[0] and int(float(vacancy.salary.salary_from)) <= int(information) <= int(float(vacancy.salary.salary_to))):
                return vacancy
            if(article == "currency" and information == str(vacancy.salary.salary).split("(")[1].split(")")[0]):
                return vacancy
            if(article != "currency" and getattr(vacancy,article) == information):
                return vacancy
            if(article == "published_at" and vacancy.published_at.split("T")[0].split("-")[2] + "." + vacancy.published_at.split("T")[0].split("-")[1] + "." + vacancy.published_at.split("T")[0].split("-")[0] == information):
                return vacancy
            return {}
        return vacancy
    
    def sorti(self, data_vacancies):
        newData = data_vacancies
        if(sortingParameter == "Оклад"):
            newData = sorted(data_vacancies, key = lambda x: (currency_to_rub[x.salary.salary_currency] * (float(x.salary.salary_from) + float(x.salary.salary_to)) / 2),reverse = True if reverseOrder == "Да" else False)
        elif(sortingParameter == "Дата публикации вакансии"):
            newData = sorted(data_vacancies, key = lambda x: x.published_at,reverse = True if reverseOrder == "Да" else False)
        elif(sortingParameter == "Навыки"):
            newData = sorted(data_vacancies, key = lambda x: len(x.key_skills) if type(x.key_skills) == list else 1, reverse = True if reverseOrder == "Да" else False)
        elif(sortingParameter == "Опыт работы"):
            newData = sorted(data_vacancies, key = lambda x: x.experience_id[3],reverse = True if reverseOrder == "Да" else False)
        elif(sortingParameter == "Премиум-вакансия"):   
            newData = sorted(data_vacancies, key = lambda x: "Да" if x.premium.upper()=="TRUE" else "Да",reverse = True if reverseOrder == "Да" else False)
        elif(sortingParameter == "Название"):
            newData = sorted(data_vacancies, key = lambda x: x.name,reverse = True if reverseOrder == "Да" else False)
        elif(sortingParameter == "Описание"):
            newData = sorted(data_vacancies, key = lambda x: x.description,reverse = True if reverseOrder == "Да" else False)
        elif(sortingParameter == "Компания"):
            newData = sorted(data_vacancies, key = lambda x: x.employer_name,reverse = True if reverseOrder == "Да" else False)
        elif(sortingParameter != ""):  
            newData = sorted(data_vacancies, key = lambda x: x.area_name,reverse = True if reverseOrder == "Да" else False)
        return newData
   
    def print_vacancies(self, data_vacancies, dic_naming):
        table = PrettyTable()   
        table.field_names = ["№"] + list(dic_naming.values())
        table._max_width = {"Название":20, "Описание":20, "Навыки":20, "Опыт работы":20, "Премиум-вакансия":20, "Компания":20, "Оклад":20, "Название региона":20, "Дата публикации вакансии":20}
        table.hrules = 1
        table.align = "l"
        number = 0
        data_vacancies = self.sorti(data_vacancies)
        for vacancy in data_vacancies:
            vacancy = self.filterVacancies(vacancy)
            number += 1
            val = [str(number)]
            if(type(vacancy) != dict):
                for item in vacancy.elements:
                    if(type(item) == list):
                        element = ('\n'.join(str(x) for x in item))
                    elif(type(item) == Salary):
                        element = item.salary
                    else:
                        element = item    
                    val.append(str(element) if (len(element) < 100) else (element[0:100] + "..."))
                date = val.pop().split("T")[0]
                val.append(date.split("-")[2] + "." + date.split("-")[1] + "." + date.split("-")[0])
            if(len(val) > 1):
                table.add_row(val)
            else:
                number -= 1
            print(vacancy.name)
        if(number == 0):
            print("Ничего не найдено")
        else:
            print(table.get_string(fields = (["№"] + (column if len(column) > 1 else list(dic_naming.values()))), start = (int(lines[0]) - 1 if len(lines) > 0 else 0), end = (int(lines[1]) - 1 if len(lines) > 1 else number)))

    def readyPrint(self):
        if(os.stat(name).st_size == 0):
            print("Пустой файл")
        elif(len(filterVacansie[0]) > 0 and len(filterVacansie) == 1):
            print("Формат ввода некорректен")
        elif(filterVacansie[0] not in fieldToEng.keys() and filterVacansie[0] != ""):
            print("Параметр поиска некорректен")
        elif(sortingParameter not in fieldToEng.keys() and sortingParameter != ""):
            print("Параметр сортировки некорректен")
        elif(reverseOrder != "Да" and reverseOrder != "Нет" and reverseOrder != ""):
            print("Порядок сортировки задан некорректно")
        else:
            a, b = DataSet.сsv_reader(name)
            if len(b) == 0 or len(a) == 0:
                print("Нет данных")
            else:
                self.print_vacancies(self.data.csv_ﬁler(a, b), fieldToRus)  

printer = InputConnect()
printer.readyPrint()


