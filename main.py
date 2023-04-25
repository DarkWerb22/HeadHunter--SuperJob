import requests
from pprint import pprint
from dotenv import load_dotenv
from terminaltables import AsciiTable
import os


def predict_rub_salary(salary_from, salary_to, salary_currency):
    if salary_currency != "RUR" and salary_currency != "rub":
        return None
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    if salary_from:
        return (salary_from) * 1.2
    if salary_to:
        return (salary_to) * 0.8

def get_vacancies(language):
    salaries = []
    url = "https://api.hh.ru/vacancies"
    page = 0
    pages_number = 1
    while page < pages_number:
        payload = {"area": 1, "text": language, "page": page}
        response = requests.get(url, params=payload)
        response.raise_for_status()
        pages_number = response.json()["pages"]
        vacancies = (response.json()["items"])
        print(page)
        for vacancie in vacancies:
            if not vacancie["salary"]:
                continue
            predicted_salary = predict_rub_salary(vacancie["salary"]["from"], vacancie["salary"]["to"], vacancie["salary"]["currency"])
            if predicted_salary:
                salaries.append(predicted_salary)
        page += 1
    vacancies_processed = len(salaries)
    average_salary = sum(salaries) // vacancies_processed
    return {
        "vacancies_found": response.json()["found"],
        "vacancies_processed": vacancies_processed,
        "average_salary": average_salary
    }
def get_vacancies_superjob(superj_token, language):
    salaries = []
    payload = {"town": "Москва", "keyword": language}
    url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id": superj_token
    }
    response = requests.get(url, params=payload, headers=headers)
    response.raise_for_status()
    #pprint(response.json()["objects"])
    for vacancie in response.json()["objects"]:
        #pprint(vacancie)
        salary_from = vacancie["payment_from"]
        salary_to = vacancie["payment_to"]
        salary_currency = vacancie["currency"]
        predict_rub_salary(salary_from, salary_to, salary_currency)
        predicted_salary = predict_rub_salary(salary_from, salary_to, salary_currency)
        if predicted_salary:
            salaries.append(predicted_salary)
    vacancies_processed = len(salaries)
    if vacancies_processed:
        average_salary = sum(salaries) // vacancies_processed
    else:
        average_salary = 0
    return {
        "vacancies_found": response.json()["total"],
        "vacancies_processed": vacancies_processed,
        "average_salary": average_salary
    }


def make_table(language_params, title):
    table_data = [
        ['языки програмирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя заркплата'],
]

    for language, params in language_params.items():
        table_data.append([language, params["vacancies_found"], params["vacancies_processed"], params["average_salary"]])
    table = AsciiTable(table_data, title)
    print(table.table)


if __name__ == "__main__":
    load_dotenv()
    superj_token = os.environ["SUPERJOB_TOKEN"]
    languages = ["python", "java", "JavaScript"]
    language_params_hh = {}
    language_params_sj = {}
    for language in languages:
        language_params_sj[language] = get_vacancies_superjob(superj_token, language)
        language_params_hh[language] = get_vacancies(language)
    #pprint(language_params_sj)
    make_table(language_params_sj, title = "SuperJob Moscow")
    make_table(language_params_hh, title = "HeadHunter Moscow")