# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы получаем должность)
# с сайтов HH(обязательно) и/или Superjob(по желанию). Приложение должно анализировать несколько страниц сайта
# (также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
# Наименование вакансии.
# Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия.

import requests
import json

resp = requests.get('https://spb.hh.ru/search/vacancy').text


def read_page_hh(page_idx, vacancy):
    params = {
        'text': vacancy, \
        'search_field': 'name', \
        'items_on_page': '100', \
        'page': page_idx
    }
    req = requests.get('https://api.hh.ru/vacancies', params=params)
    data = req.content.decode()
    req.close()
    return data


def read_vac(vacancy):
    read_vacancies = []
    for page_idx in range(0, 10):
        data = read_page_hh(page_idx, vacancy)
        jsObj = json.loads(data)
        while jsObj['items']:
            th_vacancy = jsObj['items'].pop()
            th_name = th_vacancy['name']
            th_salary = th_vacancy['salary']
            if th_salary:
                th_salary_from = th_vacancy['salary']['from']
                th_salary_to = th_vacancy['salary']['to']
                th_salary_currency = th_vacancy['salary']['currency']
            else:
                th_salary_from = '?'
                th_salary_to ='?'
                th_salary_currency = ''
            th_url_e = th_vacancy['employer']['alternate_url']
            th_url_a = th_vacancy['alternate_url']

            th_vac = {"Наименование" : th_name, "ЗП от": th_salary_from,"ЗП до": th_salary_to,"валюта": th_salary_currency,
                      "URL": th_url_a, "URL компании:": th_url_e}
            read_vacancies.append(th_vac)

    return read_vacancies


vacancy = 'Программист'
read_vacancies = read_vac(vacancy)
with open('vacances.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(read_vacancies, ensure_ascii=False, indent=4))