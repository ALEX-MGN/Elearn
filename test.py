import csv
import re
from os import walk
from multiprocessing import Pool
from practice import Report, Salary, Vacancy, AllDictionary


fieldWorkExperience = {
"noExperience": "Нет опыта",
"between1And3": "От 1 года до 3 лет",
"between3And6": "От 3 до 6 лет",
"moreThan6": "Более 6 лет"
}

class DataSet:
    """Класс который создает и рассчитывает значения для составления таблицы и статистики
    
    Attributes:
        report (class): Класс Report
        allDictionary (class): Класс AllDictionary
        file_name (str): Название файла со всеми профессиями
        profession_name (str): Название профессии, которую ищет работник
        vacancies_objects (list): Список со всеми профессиями
    """
    def __init__(self, profession = "None"):
        """Иницилизирует объект DataSet"""
        self.allDictionary = AllDictionary()
        self.profession_name = profession
        self.report = Report(self.profession_name)
        self.vacancies_objects = []

    def readystr(self, str_value):
        """Убирает в строке все лишние HTML теги
        
        Returns:
            str: Строка без HTML тегов
        
        >>> DataSet.readystr("<p>Hi</p>")
        'Hi'
        >>> DataSet.readystr("<html><head></head><p>Hi</p><body></body></html>")
        'Hi'
        """
        return ' '.join(re.sub(r"<[^>]+>", '', str_value).split())
    
    def csv_ﬁlerAndReader(self, file_name):
        """Считывает файл, все ваканскии каждого года помещает в перенную investment, а все поля для этих ваканский в переменную names,
        также заполняяет вакансию с 9 полями(параметрами вакансии)
        
        Args:
            file_name (str): Название файла с профессиями по годам

        Returns:
            dict: Словарь с ключом - год, а значение - список всех вакансий
        """
        names = []
        investment = []
        vacancies_objects = []
        with open("newCSV/" + file_name, encoding="UTF-8-sig") as File:
            reader = csv.reader(File, delimiter=',')
            for row in reader:
                if(len(names) == 0):
                    names = row
                elif(len(names) == len(row) and not("" in row)):
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
            return {vacancy.published_at[0][0:4]:vacancies_objects}

    def countsNumberAndSalary(self, everyYear):
        """Функция считает количество ваканский в каждом году, сумму всех зарплат, количество ваканский(которую просят) в каждом году,
        сумму зарплат ваканский(которую просят) в каждом году
        
        Args:
            everyYear (dict): Словарь с ключом - год, а значение - список всех вакансий

        Returns:
            list: Возвращает список из 6 элементов: Год, количество всех вакансий, сумму зарплат всех вакансий, количество нужных вакансий, сумму зарплат нужных вакансий, все вакансии
        """
        sumAverageSalary = 0

        countAverageSalaryForProfession = 0
        sumAverageSalaryForProfession = 0
        for vacancie in list(everyYear.values())[0]:
            sumAverageSalary += vacancie.mysalary
            if(self.profession_name in vacancie.name[0]):
                countAverageSalaryForProfession += 1
                sumAverageSalaryForProfession += vacancie.mysalary   
        return [list(everyYear.keys())[0],len(list(everyYear.values())[0]), sumAverageSalary, countAverageSalaryForProfession, sumAverageSalaryForProfession, list(everyYear.values())[0]]    
    
    def calculating_average_salary(self):
        """Функция считает значения среднии зарплаты в разных городах, долю ваканский в каждом городе относительно всех вакансий"""
        dicti3 = self.allDictionary.dictionary_level_salaries_cities
        for salaryYear in dicti3.keys():
            dicti3[salaryYear] = int(int(dicti3[salaryYear].split(" ")[1]) / int(dicti3[salaryYear].split(" ")[0]))
        dicti4 = self.allDictionary.dictionary_vacancy_rate_city
        for salaryYear in dicti4.keys(): 
            dicti4[salaryYear] = round(dicti4[salaryYear] / len(self.vacancies_objects), 4)

    def readyPrint(self, listWithSumSalaryAndCount):
        """Функция сначала считает заполняет словари с городами,
        потом выводит всю статистику, формирует графики,excel,pdf файлы
        
        Args:
            listWithSumSalaryAndCount (list): Cписок из 6 элементов: Год, количество всех вакансий, сумму зарплат всех вакансий, количество нужных вакансий, сумму зарплат нужных вакансий, все вакансии
        """
        for statisticForYear in listWithSumSalaryAndCount:
            self.vacancies_objects += statisticForYear[5]
            if(statisticForYear[0] in self.allDictionary.dictionary_salary_levels):
                #1 заполнения словаря Динамика уровня зарплат по годам
                self.allDictionary.dictionary_salary_levels[statisticForYear[0]] += int(statisticForYear[2] / statisticForYear[1])
                self.report.dictionary_salary_levels = self.allDictionary.dictionary_salary_levels
                #2 заполнения словаря Динамика количества вакансий по годам
                self.allDictionary.dictionary_number_vacancies[statisticForYear[0]] += statisticForYear[1]
                self.report.dictionary_number_vacancies = self.allDictionary.dictionary_number_vacancies
                #3 заполнения словаря Динамика уровня зарплат по годам для выбранной профессии
                self.allDictionary.dictionary_salary_levels_profession[statisticForYear[0]] += int(statisticForYear[4] / statisticForYear[3])
                self.report.dictionary_salary_levels_profession = self.allDictionary.dictionary_salary_levels_profession
                #4 заполнения словаря Динамика количества вакансий по годам для выбранной профессии
                self.allDictionary.dictionary_number_vacancies_profession[statisticForYear[0]] += statisticForYear[3]
                self.report.dictionary_number_vacancies_profession = self.allDictionary.dictionary_number_vacancies_profession
            else:
                #1 заполнения словаря Динамика уровня зарплат по годам
                self.allDictionary.dictionary_salary_levels[statisticForYear[0]] = int(statisticForYear[2] / statisticForYear[1])
                self.report.dictionary_salary_levels = self.allDictionary.dictionary_salary_levels
                #2 заполнения словаря Динамика количества вакансий по годам
                self.allDictionary.dictionary_number_vacancies[statisticForYear[0]] = statisticForYear[1]
                self.report.dictionary_number_vacancies = self.allDictionary.dictionary_number_vacancies
                #3 заполнения словаря Динамика уровня зарплат по годам для выбранной профессии
                self.allDictionary.dictionary_salary_levels_profession[statisticForYear[0]] = int(statisticForYear[4] / statisticForYear[3])
                self.report.dictionary_salary_levels_profession = self.allDictionary.dictionary_salary_levels_profession
                #4 заполнения словаря Динамика количества вакансий по годам для выбранной профессии
                self.allDictionary.dictionary_number_vacancies_profession[statisticForYear[0]] = statisticForYear[3]
                self.report.dictionary_number_vacancies_profession = self.allDictionary.dictionary_number_vacancies_profession

        for vacancie in self.vacancies_objects:
            #заполнения словаря с средней зарплатой по городам
            if (vacancie.area_name[0] in self.allDictionary.dictionary_level_salaries_cities.keys()):
                count = int(self.allDictionary.dictionary_level_salaries_cities[vacancie.area_name[0]].split(" ")[0]) + 1
                money = int(self.allDictionary.dictionary_level_salaries_cities[vacancie.area_name[0]].split(" ")[1]) + vacancie.mysalary
                self.allDictionary.dictionary_level_salaries_cities[vacancie.area_name[0]] = str(count) + " " + str(money)  
            else:
                self.allDictionary.dictionary_level_salaries_cities[vacancie.area_name[0]] = "1" + " " + str(vacancie.mysalary)
            #заполнения словаря: доля ваканский каждого города относительно всех вакансий
            if (vacancie.area_name[0] in self.allDictionary.dictionary_vacancy_rate_city.keys()):
                self.allDictionary.dictionary_vacancy_rate_city[vacancie.area_name[0]] += 1
            else:
                self.allDictionary.dictionary_vacancy_rate_city[vacancie.area_name[0]] = 1
        self.calculating_average_salary()

        print("Динамика уровня зарплат по годам: ",end="")
        self.report.dictionary_salary_levels = self.allDictionary.dictionary_salary_levels
        print(self.allDictionary.dictionary_salary_levels)
        print("Динамика количества вакансий по годам: ",end="")
        self.report.dictionary_number_vacancies = self.allDictionary.dictionary_number_vacancies
        print(self.allDictionary.dictionary_number_vacancies)
        print("Динамика уровня зарплат по годам для выбранной профессии: ",end="")
        self.report.dictionary_salary_levels_profession = self.allDictionary.dictionary_salary_levels_profession
        print(self.allDictionary.dictionary_salary_levels_profession)
        print("Динамика количества вакансий по годам для выбранной профессии: ",end="")
        self.report.dictionary_number_vacancies_profession = self.allDictionary.dictionary_number_vacancies_profession
        print(self.allDictionary.dictionary_number_vacancies_profession)  
        print("Уровень зарплат по городам (в порядке убывания): ",end="")
        self.dictionary_level_salaries_cities = dict(sorted(filter(lambda x: self.allDictionary.dictionary_vacancy_rate_city[x[0]] >= 0.01, self.allDictionary.dictionary_level_salaries_cities.items()), key=lambda item: item[1], reverse=True)[:10])
        self.report.dictionary_level_salaries_cities = self.dictionary_level_salaries_cities
        print(self.dictionary_level_salaries_cities)
        print("Доля вакансий по городам (в порядке убывания): ",end="")
        self.dictionary_vacancy_rate_city = dict(sorted(filter(lambda x: self.allDictionary.dictionary_vacancy_rate_city[x[0]] >= 0.01, self.allDictionary.dictionary_vacancy_rate_city.items()), key=lambda item: item[1], reverse=True)[:10])
        self.report.dictionary_vacancy_rate_city = self.dictionary_vacancy_rate_city
        print(self.dictionary_vacancy_rate_city)
        
        self.report.generate_pdf()
        self.report.generate_graphics()
        self.report.generate_excel()

    def runningFunctionsInMultiThread(self, fileNames):
        """Функция запускает другие функции в многопотоке

        Args:
            fileNames (list): Список с названиями всех файлов csv

        Returns:
            listWithSumSalaryAndCount (list): Cписок из 6 элементов: Год, количество всех вакансий, сумму зарплат всех вакансий, количество нужных вакансий, сумму зарплат нужных вакансий, все вакансии
        """
        pool = Pool(10)
        vacanciesDividedByYear = pool.map(self.csv_ﬁlerAndReader, fileNames)
        listWithSumSalaryAndCount = pool.map(self.countsNumberAndSalary, vacanciesDividedByYear)
        return listWithSumSalaryAndCount

if __name__ == '__main__':
    folderName = input("Введите название папки: ")
    profession = input("Введите название профессии: ")
    fileNames = [] 

    for (dirpath, dirnames, filenames) in walk(folderName):
        fileNames.extend(filenames)
        break

    printer = DataSet(profession)
    listWithSumSalaryAndCount = printer.runningFunctionsInMultiThread(fileNames)   
    printer.readyPrint(listWithSumSalaryAndCount)
