import csv
import re
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
import pdfkit
import doctest
import cProfile
import multiprocessing
import concurrent.futures
import requests
import xmltodict
from os import walk
from datetime import datetime
from openpyxl import Workbook
import multiprocessing
from prettytable import PrettyTable
from openpyxl.styles import Border, Side, Font
from jinja2 import Environment, FileSystemLoader


names = []
investment = []

"""Словарь по переводу валюты в рубли"""
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
    "": 0,
}

currencyCode = {
    "USD": "R01235",
    "EUR": "R01239",
    "KZT": "R01335",
    "UAH": "R01720", 
    "BYR": "R01090",
    "UZS": "R01717",
}

"""Перевод переменных на анлийский язык"""
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

"""Перевод переменных на русский язык"""
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

"""Расшифрования сокращения валют"""
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

"""Перевод переменной опыта в текст"""
fieldWorkExperience = {
"noExperience": "Нет опыта",
"between1And3": "От 1 года до 3 лет",
"between3And6": "От 3 до 6 лет",
"moreThan6": "Более 6 лет"
}

class AllDictionary:
    """Класс со всеми нужными словарями для вывода статистики
    Attributes:
        dictionary_salary_levels (dict): Динамика уровня зарплат по годам
        dictionary_number_vacancies (dict): Динамика количества вакансий по годам
        dictionary_salary_levels_profession (dict): Динамика уровня зарплат по годам для выбранной профессии
        dictionary_number_vacancies_profession (dict): Динамика количества вакансий по годам для выбранной профессии
        dictionary_level_salaries_cities (dict): Уровень зарплат по городам (в порядке убывания)
        dictionary_vacancy_rate_city (dict): Доля вакансий по городам (в порядке убывания)
        dictionary_currency (dict): Количество разынх валют 
    """
    def __init__(self):
        """Иницилизирует объект AllDictionary"""

        """self.dictionary_salary_levels = {}
        self.dictionary_number_vacancies = {}
        self.dictionary_salary_levels_profession = {}
        self.dictionary_number_vacancies_profession = {}
        self.dictionary_level_salaries_cities = {}
        self.dictionary_vacancy_rate_city = {}"""
        self.dictionary_currency = {}
        self.dictionary_currency_frequency = {}
        
class Salary:
    """Класс со всеми значениями зарплаты
    
    Attributes:
        salary_from (list): Минимальное значение зарплаты
        salary_to (list): Максимальное значение зарплаты
        salary_gross (list): Наличие или отсутсвие включенных налогов
        salary_currency (list): Валюта в которой будет выплачиваться зарплата
        salary (str): Красивый вывод зарплаты
    """
    def __init__(self, salary_from, salary_to, salary_gross, salary_currency):
        """Иницилизирует объект Salary, переделывает все переменные,кроме salary в массив из одного элемента
        Args:
            salary_from (str): Минимальное значение зарплаты
            salary_to (str): Максимальное значение зарплаты
            salary_gross (str): Наличие или отсутсвие включенных налогов
            salary_currency (str): Валюта в которой будет выплачиваться зарплата
        
        >>> Salary(10000, 20000, "Yes", 'EUR').salary_from
        [10000]
        >>> type(Salary(10000, 20000.0, "Yes", 'EUR')).__name__
        'Salary'
        """
        self.salary_from = [0] if salary_from == "" else [salary_from]
        self.salary_to = [0] if salary_to == "" else [salary_to]
        self.salary_gross = [salary_gross]
        self.salary_currency = [salary_currency]

class Vacancy:
    """Класс со всеми значениями зарплаты
    
    Attributes:
        name (arr): Название профессии
        area_name (arr): Компания, предоставляющая вакансию
        published_at (arr): Время публикации вакансии
        description (arr): Описание вакансии
        key_skills (arr): Навыки, которыми нужно обладать работнику
        experience_id (arr): Опыт работы
        premiumм (arr): Премиум или нет вакансия
        employer_name (arr): Название региона
        salary (class): Класс Зарплаты
        elements (arr): Все значение в одной переменной
    """
    def __init__(self, name, area_name, published_at, description, key_skills, experience_id, premium, employer_name, salary):
        """Иницилизирует объект Vacancy, переделывает все переменные,кроме salary в массив из одного элемента
        
        Args:
            name (str): Название профессии
            area_name (str): Компания, предоставляющая вакансию
            published_at (str): Время публикации вакансии
            description (str): Описание вакансии
            key_skills (str): Навыки, которыми нужно обладать работнику
            experience_id (str): Опыт работы
            premium (str): Премиум или нет вакансия
            employer_name (str): Название региона
            salary (str): Класс Зарплаты
        >>> Vacancy("Программист", "Компас-Плюс", "22.11.2022", "Описание", "Программирование", "between3And6", "Yes", "Новосибирск", Salary(10000, 20000.0, "Yes", 'RUR')).name
        ['Программист']
        >>> type(Vacancy("Программист", "Компас-Плюс", "22.11.2022", "Описание", "Программирование", "between3And6", "Yes", "Новосибирск", Salary(10000, 20000.0, "Yes", 'RUR'))).__name__
        'Vacancy'
        """
        self.name = [name]
        self.area_name = [area_name] 
        self.published_at = [published_at]
        self.description = [description]
        self.key_skills = key_skills
        self.experience_id = [experience_id]
        self.premium = [premium]
        self.employer_name = [employer_name]
        self.salary = salary
        self.elements=[name,description,key_skills,experience_id,premium,employer_name,salary,area_name,published_at]

class DataSet:
    """Класс который создает и рассчитывает значения для составления таблицы и статистики
    
    Attributes:
        allDictionary (class): Класс AllDictionary
        file_name (str): Название файла со всеми профессиями
        profession_name (str): Название профессии, которую ищет работник
        vacancies_objects (list): Список со всеми профессиями
    """
    def __init__(self, profession = "None", fileNames = []):
        """Иницилизирует объект DataSet"""
        self.allDictionary = AllDictionary()
        self.profession_name = profession
        self.vacancies_objects = []
        self.fileNames = fileNames

    def readystr(self, str_value):
        """Убирает в строке все лишние HTML теги
        
        Returns:
            str: Строка без HTML тегов
        
        >>> DataSet().readystr("<p>Hi</p>")
        'Hi'
        >>> DataSet().readystr("<html><head></head><p>Hi</p><body></body></html>")
        'Hi'
        """
        return ' '.join(re.sub(r"<[^>]+>", '', str_value).split())
    
    def csv_ﬁlerAndReader(self, file_name):
        """Считывает файл, все ваканскии каждого года помещает в перенную investment, а все поля для этих ваканский в переменную names,
        также заполняяет вакансию с 9 полями(параметрами вакансии), вызывает функцию countsNumberAndSalary, которая считает данные для статистики
        
        Args:
            file_name (str): Название файла с профессиями по годам
        Returns:
            list: Возвращает список из 6 элементов: Год, количество всех вакансий, сумму зарплат всех вакансий, количество нужных вакансий, сумму зарплат нужных вакансий, все вакансии
        """
        names = []
        investment = []
        vacancies_objects = []
        with open("newCSV/" + file_name, encoding="UTF-8-sig") as File:
            reader = csv.reader(File, delimiter=',')
            for row in reader:
                if(len(names) == 0):
                    names = row
                elif(len(names) == len(row)):
                    investment.append(row)

            for element in investment:
                salary = ["", "", "", ""]
                array = ["","","","","","","","",""]
                namesIndex = ["name", "area_name", "published_at", "description", "key_skills", "experience_id", "premium", "employer_name", "salary"]
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
                            arrayWithoutTegs.append(self.readystr(word))
                    if(len(arrayWithoutTegs) == 1):
                        arrayWithoutTegs = arrayWithoutTegs[0]
                    if(names[item] == "salary_from"):
                        salary[0] = arrayWithoutTegs
                    elif(names[item] == "salary_to"):
                        salary[1] = arrayWithoutTegs
                    elif(names[item] == "salary_gross"):
                        salary[2] = arrayWithoutTegs
                    elif(names[item] == "salary_currency"):
                        salary[3] = arrayWithoutTegs
                        readySalary = Salary(*salary)
                        array[8] = readySalary
                    else:
                        array[namesIndex.index(names[item])] = arrayWithoutTegs
                vacancy = Vacancy(*array)
                vacancies_objects.append(vacancy)
            return vacancies_objects

    def getCurrency(self):
        all_dict_data = {"DATE": [], "USD": [], "EUR": [], "KZT": [], "UAH": [], "BYR": []}
        for currencyValue in self.allDictionary.dictionary_currency.keys():
            if(currencyValue != "" and currencyValue != "RUR" and self.allDictionary.dictionary_currency[currencyValue] > 5000):
                #int(self.fileNames[len(self.fileNames) - 1][10:14]) + 1
                for year in range(int(self.fileNames[0][10:14]),2005):
                    for month in range(1,13):
                        month = ("0" + str(month))[-2:]
                        for day in range(1, 29):
                            day = ("0" + str(day))[-2:]
                            date = f"{day}/{month}/{year}"
                            if(f"{year}-{month}" not in all_dict_data["DATE"]):
                                all_dict_data["DATE"].append(f"{year}-{month}")
                            response = requests.get(f'http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={date}&date_req2={date}&VAL_NM_RQ={currencyCode[currencyValue]}')
                            dict_data = xmltodict.parse(response.content)
                            if("Record" in dict_data["ValCurs"]):
                                all_dict_data[currencyValue].append(round(float(dict_data["ValCurs"]['Record']["Value"].replace(",",".")) / float(dict_data["ValCurs"]['Record']["Nominal"].replace(",",".")),2))
                                break
                            if(day == 28):
                                all_dict_data[currencyValue].append("-")

        df = pd.DataFrame(data = {"DATE": all_dict_data["DATE"],"USD":all_dict_data["USD"],"EUR":all_dict_data["EUR"],"KZT":all_dict_data["KZT"],"UAH":all_dict_data["UAH"],"BYR":all_dict_data["BYR"]}) 
        df.to_csv("dataFrame",index=False)

    def readyPrint(self, listWithSumSalaryAndCount):
        """Функция сначала считает заполняет словари с городами,
        потом выводит всю статистику, формирует графики,excel,pdf файлы
        
        Args:
            listWithSumSalaryAndCount (list): Cписок из 6 элементов: Год, количество всех вакансий, сумму зарплат всех вакансий, количество нужных вакансий, сумму зарплат нужных вакансий, все вакансии
        """
        for vacancyForYear in listWithSumSalaryAndCount:  
            for vacancy in vacancyForYear:  
                if(vacancy.salary.salary_currency[0] in self.allDictionary.dictionary_currency.keys()):
                    self.allDictionary.dictionary_currency[vacancy.salary.salary_currency[0]] += 1
                else:
                    self.allDictionary.dictionary_currency[vacancy.salary.salary_currency[0]] = 1
        print("Частотность с которой встречаются различные валюты ", self.allDictionary.dictionary_currency)
        for item in self.allDictionary.dictionary_currency.items():
            self.allDictionary.dictionary_currency_frequency[item[0]] = round(item[1] / sum(self.allDictionary.dictionary_currency.values()), 3)
        print("Процент с которой встречаются различные валюты ",self.allDictionary.dictionary_currency_frequency)

    def runningFunctionsInMultiThread(self, fileNames):
        """Функция запускает другие функции в многопотоке
        Args:
            fileNames (list): Список с названиями всех файлов csv
        Returns:
            listWithSumSalaryAndCount (list): Cписок из 6 элементов: Год, количество всех вакансий, сумму зарплат всех вакансий, количество нужных вакансий, сумму зарплат нужных вакансий, все вакансии
        """
        aallVacancies = []
        with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(self.csv_ﬁlerAndReader, fileName): fileName for fileName in fileNames}
            for fut in concurrent.futures.as_completed(futures):
                aallVacancies.append(fut.result())
        return aallVacancies

def main():
    #folderName = input("Введите название папки: ")
    #profession = input("Введите название профессии: ")
    folderName = "newCSV"
    profession = "Программист"
    fileNames = [] 

    for (dirpath, dirnames, filenames) in walk(folderName):
        fileNames.extend(filenames)
        break

    printer = DataSet(profession, fileNames)
    listWithSumSalaryAndCount = printer.runningFunctionsInMultiThread(fileNames)   
    printer.readyPrint(listWithSumSalaryAndCount)
    printer.getCurrency()

if __name__ == "__main__":
    doctest.testmod()
    cProfile.run('main()')