# Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
# (необходимо анализировать оба поля зарплаты).

from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['db_vacancies']
vacancies = db.vacancies

min_salary = 100000

for vacancy in vacancies.find({'$or' : [{'ЗП от': {'$gt': min_salary}}, {'ЗП до': {'$gt': min_salary}}]}):
    pprint(vacancy)
    #  выведет и те, что в другой валюте указаны (рубли/евро/...). Не выведет, где не указана ЗП