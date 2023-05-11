import os

import requests
from dotenv import load_dotenv
from terminaltables import AsciiTable


def predict_rub_salary(salary_from, salary_to, salary_currency):
    if salary_currency != "RUR" and salary_currency != "rub":
        return None
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    if salary_from:
        return salary_from * 1.2
    if salary_to:
        return salary_to * 0.8


def get_vacancies_statiscics_hh(language):
    salaries = []
    url = "https://api.hh.ru/vacancies"
    page = 0
    pages_number = 1
    while page < pages_number:
        area_id = 1
        payload = {"area": area_id, "text": language, "page": page}
        response = requests.get(url, params=payload)
        response.raise_for_status()
        response_content = response.json()
        pages_number = response_content["pages"]
        vacancies = response_content["items"]
        for vacancy in vacancies:
            if not vacancy["salary"]:
                continue
            predicted_salary = predict_rub_salary(vacancy["salary"]["from"], vacancy["salary"]["to"],
                                                  vacancy["salary"]["currency"])
            if predicted_salary:
                salaries.append(predicted_salary)
        page += 1
    vacancies_processed = len(salaries)
    average_salary = sum(salaries) // vacancies_processed
    return {
        "vacancies_found": response_content["found"],
        "vacancies_processed": vacancies_processed,
        "average_salary": average_salary
    }


def get_vacancies_statistics_sj(superj_token, language):
    salaries = []
    url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id": superj_token
    }
    page = 1
    while True:
        payload = {"town": "Москва", "keyword": language, "page": page}
        response = requests.get(url, params=payload, headers=headers)
        response.raise_for_status()
        response_content = response.json()
        for vacancie in response_content["objects"]:
            salary_from = vacancie["payment_from"]
            salary_to = vacancie["payment_to"]
            salary_currency = vacancie["currency"]
            predicted_salary = predict_rub_salary(salary_from, salary_to, salary_currency)
            if predicted_salary:
                salaries.append(predicted_salary)
        if not response_content["more"]:
            break
        else:
            page += 1
    vacancies_processed = len(salaries)
    if vacancies_processed:
        average_salary = sum(salaries) // vacancies_processed
    else:
        average_salary = 0
    return {
        "vacancies_found": response_content["total"],
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
        language_params_sj[language] = get_vacancies_statistics_sj(superj_token, language)
        #language_params_hh[language] = get_vacancies_statiscics_hh(language)
    make_table(language_params_sj, title="SuperJob Moscow")
    make_table(language_params_hh, title="HeadHunter Moscow")