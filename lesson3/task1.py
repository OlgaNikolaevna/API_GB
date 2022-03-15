# Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# которая будет добавлять только новые вакансии/продукты в вашу базу.

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import hh_vacancies as hh

client = MongoClient('127.0.0.1', 27017)
db = client['db_vacancies']
vacancies = db.vacancies


def add_vacancy(vacancy):
    try:
        vacancies.insert_one(vacancy)
    except DuplicateKeyError:
        print('Vacancy is already exist')


vacancy = 'Программист'
read_vacancies = hh.read_vac(vacancy)
for vac in read_vacancies: #лучше, наверное, сразу по прочтению добавлять. Не грузтить оперативную память
    add_vacancy(vac)

