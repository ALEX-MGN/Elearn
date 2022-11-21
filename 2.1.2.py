import csv
import matplotlib.pyplot as plt
import numpy as np

name = input("Введите название файла: ") 
profession = input("Введите название профессии: ")

names = []
investment = []

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

class AllDictionary:
    def __init__(self):
        self.dictionary_salary_levels = {}
        self.dictionary_number_vacancies = {}
        self.dictionary_salary_levels_profession = {}
        self.dictionary_number_vacancies_profession = {}
        self.dictionary_level_salaries_cities = {}
        self.dictionary_vacancy_rate_city = {}
        
class Vacancy:
    def __init__(self, name, salary_from, salary_to, salary_currency, area_name, published_at, salary_gross, description, key_skills, experience_id, premium, employer_name, salary):
        self.name = name
        self.salary_from = salary_from 
        self.salary_to = salary_to
        self.salary_currency = salary_currency 
        self.mysalary = int(currency_to_rub[salary_currency[0]] * (float(salary_from[0]) + float(salary_to[0])))
        self.area_name = area_name 
        self.published_at = published_at
        self.salary_gross = salary_gross
        self.published_at = published_at
        self.description = description
        self.key_skills = key_skills
        self.experience_id = experience_id
        self.premium = premium
        self.employer_name = employer_name
        self.salary = salary
        
class DataSet:
    def __init__(self):
        self.report = Report()
        self.allDictionary = AllDictionary()
        self.file_name = name
        self.profession_name = profession
        self.vacancies_objects = []

    def сsv_reader(self,ﬁle_name): 
        global names
        with open(ﬁle_name, encoding="UTF-8-sig") as File:
            reader = csv.reader(File, delimiter=',')
            for row in reader:
                if(len(names) == 0):
                    names = row
                elif(len(names) == len(row) and not("" in row)):
                    investment.append(row)
        return investment, names

    def csv_ﬁler(self, reader):
        for element in reader:
            array = ["","","","","","","","","","","","",""]
            namesIndex = ["name", "salary_from", "salary_to", "salary_currency", "area_name", "published_at", "salary_gross", "description", "key_skills", "experience_id", "premium", "employer_name", "salary"]
            for item in range(len(names)):
                value = element[item]
                value = value.split("\n") if ("\n" in value) else [value]
                array[namesIndex.index(names[item])] = value
            vacancy = Vacancy(*array)
            self.vacancies_objects.append(vacancy)
        return self.vacancies_objects

    def completion_dictionary(self):
        for vacancie in self.vacancies_objects:
            #1 вывод
            if (int(vacancie.published_at[0][0:4]) in self.allDictionary.dictionary_salary_levels.keys()):
                count = int(self.allDictionary.dictionary_salary_levels[int(vacancie.published_at[0][0:4])].split(" ")[0]) + 1
                money = int(self.allDictionary.dictionary_salary_levels[int(vacancie.published_at[0][0:4])].split(" ")[1]) + vacancie.mysalary
                self.allDictionary.dictionary_salary_levels[int(vacancie.published_at[0][0:4])] = str(count) + " " + str(money)
            else:
                self.allDictionary.dictionary_salary_levels_profession[int(vacancie.published_at[0][0:4])] = "0" + " " + "0"
                self.allDictionary.dictionary_salary_levels[int(vacancie.published_at[0][0:4])] = "1" + " " + str(vacancie.mysalary)
            #2 вывод
            if (int(vacancie.published_at[0][0:4]) in self.allDictionary.dictionary_number_vacancies.keys()):
                self.allDictionary.dictionary_number_vacancies[int(vacancie.published_at[0][0:4])] += 1
            else:
                self.allDictionary.dictionary_number_vacancies_profession[int(vacancie.published_at[0][0:4])] = 0
                self.allDictionary.dictionary_number_vacancies[int(vacancie.published_at[0][0:4])] = 1
            #3 вывод
            if(profession in vacancie.name[0]):
                if (int(vacancie.published_at[0][0:4]) in self.allDictionary.dictionary_salary_levels_profession.keys()):
                    count = int(self.allDictionary.dictionary_salary_levels_profession[int(vacancie.published_at[0][0:4])].split(" ")[0]) + 1
                    money = int(self.allDictionary.dictionary_salary_levels_profession[int(vacancie.published_at[0][0:4])].split(" ")[1]) + vacancie.mysalary
                    self.allDictionary.dictionary_salary_levels_profession[int(vacancie.published_at[0][0:4])] = str(count) + " " + str(money)
                else:
                    self.allDictionary.dictionary_salary_levels_profession[int(vacancie.published_at[0][0:4])] = "1" + " " + str(vacancie.mysalary)
            #4 вывод
            if(profession in vacancie.name[0]):
                if (int(vacancie.published_at[0][0:4]) in self.allDictionary.dictionary_number_vacancies_profession.keys()):
                    self.allDictionary.dictionary_number_vacancies_profession[int(vacancie.published_at[0][0:4])] += 1
                else:
                    self.allDictionary.dictionary_number_vacancies_profession[int(vacancie.published_at[0][0:4])] = 1
            #5 вывод
            if (vacancie.area_name[0] in self.allDictionary.dictionary_level_salaries_cities.keys()):
                count = int(self.allDictionary.dictionary_level_salaries_cities[vacancie.area_name[0]].split(" ")[0]) + 1
                money = int(self.allDictionary.dictionary_level_salaries_cities[vacancie.area_name[0]].split(" ")[1]) + vacancie.mysalary
                self.allDictionary.dictionary_level_salaries_cities[vacancie.area_name[0]] = str(count) + " " + str(money)  
            else:
                self.allDictionary.dictionary_level_salaries_cities[vacancie.area_name[0]] = "1" + " " + str(vacancie.mysalary)
            #6 вывод
            if (vacancie.area_name[0] in self.allDictionary.dictionary_vacancy_rate_city.keys()):
                self.allDictionary.dictionary_vacancy_rate_city[vacancie.area_name[0]] += 1
            else:
                self.allDictionary.dictionary_vacancy_rate_city[vacancie.area_name[0]] = 1

    def calculating_average_salary(self):
        dicti = self.allDictionary.dictionary_salary_levels
        for salaryYear in dicti.keys():
            dicti[salaryYear] = int(int(dicti[salaryYear].split(" ")[1]) / (int(dicti[salaryYear].split(" ")[0]) * 2))
        dicti2 = self.allDictionary.dictionary_salary_levels_profession
        for salaryYear in dicti2.keys():
            if(int(dicti2[salaryYear].split(" ")[0]) != 0):
                dicti2[salaryYear] = int(int(dicti2[salaryYear].split(" ")[1]) / (int(dicti2[salaryYear].split(" ")[0]) * 2))
            else:
                dicti2[salaryYear] = 0
        dicti3 = self.allDictionary.dictionary_level_salaries_cities
        for salaryYear in dicti3.keys():
            dicti3[salaryYear] = int(int(dicti3[salaryYear].split(" ")[1]) / (int(dicti3[salaryYear].split(" ")[0]) * 2))
        dicti4 = self.allDictionary.dictionary_vacancy_rate_city
        for salaryYear in dicti4.keys():
            dicti4[salaryYear] = round(dicti4[salaryYear] / len(self.vacancies_objects), 4)

    def readyPrint(self):
        a, b = self.сsv_reader(name)
        self.csv_ﬁler(a)
        self.completion_dictionary()
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
        self.report.generate_excel()



class Report:
    def __init__(self):
        self.dictionary_salary_levels = {}
        self.dictionary_number_vacancies = {}
        self.dictionary_salary_levels_profession = {}
        self.dictionary_number_vacancies_profession = {}
        self.dictionary_level_salaries_cities = {}
        self.dictionary_vacancy_rate_city = {}

    def generate_excel(self):
        plt.rcParams.update({'font.size': 8})
        #1 ГРАФИК
        labelsLevel = self.dictionary_salary_levels.keys()
        middle_salary = self.dictionary_salary_levels.values()
        middle_salary_profession = self.dictionary_salary_levels_profession.values()

        x = np.arange(len(labelsLevel))  
        width = 0.35 

        ax = plt.subplot(221)
        ax.bar(x - width/2, middle_salary, width, label='средняя з/п')
        ax.bar(x + width/2, middle_salary_profession, width, label='з/п ' + profession)
        ax.set_title('Уровень зарплат по годам')
        ax.set_xticks(x, labelsLevel, rotation = 90)
        plt.grid(axis='y')
        ax.legend()
        #2 ГРАФИК
        labelsCount = self.dictionary_number_vacancies.keys()
        middle_count = self.dictionary_number_vacancies.values()
        middle_count_profession = self.dictionary_number_vacancies_profession.values()

        x = np.arange(len(labelsCount))  
        width = 0.35 

        ax = plt.subplot(222)
        ax.bar(x - width/2, middle_count, width, label='Количества вакансий')
        ax.bar(x + width/2, middle_count_profession, width, label='Количества вакансий \n' + profession)
        ax.set_title('Количество вакансий по годам')
        ax.set_xticks(x, labelsCount, rotation = 90)
        plt.grid(axis='y')
        ax.legend()
        #3 ГРАФИК
        ax = plt.subplot(223)
        ax.set_title('Уровень зарплат по городам')
        plt.rcParams.update({'font.size': 6})
        city = self.dictionary_level_salaries_cities.keys()
        y_pos = np.arange(len(city))
        performance = self.dictionary_level_salaries_cities.values()

        ax.barh(y_pos, performance,  align = 'center')
        ax.set_yticks(y_pos, labels = city)
        ax.invert_yaxis() 
        
        plt.grid(axis='x')

        #4 ГРАФИК   
        ax = plt.subplot(224)
        plt.rcParams.update({'font.size': 8})
        ax.set_title('Доля вакансий по городам')
        plt.rcParams.update({'font.size': 6})
        ax.pie(list(self.dictionary_vacancy_rate_city.values()) + [1 - sum(self.dictionary_vacancy_rate_city.values())], labels = list(self.dictionary_vacancy_rate_city.keys()) + ["Другие"])

        plt.subplots_adjust(wspace = 0.5, hspace = 0.5)
        plt.savefig("Graphics", dpi = 200, bbox_inches='tight')

printer = DataSet()
printer.readyPrint()
