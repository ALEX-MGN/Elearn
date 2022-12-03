from unittest import TestCase
from practice import Salary, Vacancy, DataSet, InputConnect, Report

class SalaryTests(TestCase):
    def test_salary_salary_from(self):
        self.assertEqual(Salary(10000, 20000, "Yes", 'EUR').salary_from, [10000])
    def test_salary_salary(self):
        self.assertEqual(Salary(10000, 20000.0, "Yes", 'EUR').salary, '10 000 - 20 000 (Евро) (С вычетом налогов)')
    def test_salary_type(self):
        self.assertEqual(type(Salary(10000, 20000.0, "Yes", 'EUR')).__name__, 'Salary')

class VacancyTests(TestCase):
    def test_vacancy_mysalary(self):
        self.assertEqual(Vacancy("Программист", "Компас-Плюс", "22.11.2022", "Описание", "Программирование", "between3And6", "Yes", "Новосибирск", Salary(10000, 20000.0, "Yes", 'RUR')).mysalary, 30000)
    def test_vacancy_name(self):
        self.assertEqual(Vacancy("Программист", "Компас-Плюс", "22.11.2022", "Описание", "Программирование", "between3And6", "Yes", "Новосибирск", Salary(10000, 20000.0, "Yes", 'RUR')).name, ['Программист'])
    def test_vacancy_type(self):
        self.assertEqual(type(Vacancy("Программист", "Компас-Плюс", "22.11.2022", "Описание", "Программирование", "between3And6", "Yes", "Новосибирск", Salary(10000, 20000.0, "Yes", 'RUR'))).__name__, 'Vacancy')

class DataSetTests(TestCase):
    def test_dataSet_readystr(self):
        self.assertEqual(DataSet.readystr("<html><head></head><p>Hi</p><body></body></html>"), 'Hi')
    def test_dataSet_readystrOneTag(self):
        self.assertEqual(DataSet.readystr("<p>Hi</p>"), 'Hi')


class InputConnectTests(TestCase):
    def test_inputConnect_filterVacancies(self):
        filterVacansie = ["Идентификатор валюты оклада", "Рубли"]
        vacancy = Vacancy("Программист", "Компас-Плюс", "22.11.2022", "Описание", "Программирование", "between3And6", "Yes", "Новосибирск", Salary(10000, 20000.0, "Yes", 'EUR'))
        self.assertEqual(InputConnect().filterVacancies(vacancy, filterVacansie), {})

class ReportTests(TestCase):
    def test_dataSet_generate_table(self):
        profession = "Программист"
        self.assertEqual(Report().generate_table(profession), "<table class='main_table'><tr><th>Год</th><th>Средняя зарплата</th><th>Средняя зарплата - Программист</th><th>Количество вакансий</th><th>Количество вакансий - Программист</th></tr></tr></table><h1>Статистика по городам</h1><table class='tableCity1'><tr><th>Город</th><th>Уровень зарплат</th></tr></table><table class='tableCity2'><tr><th>Город</th><th>Уровень зарплат</th></tr></table>")