import requests


# ---------------------------------------------------------
# ФУНКЦИЯ ДЛЯ ПОИСКА ВАКАНСИЙ ЧЕРЕЗ API HH.RU
# ---------------------------------------------------------
def get_vacancies(search_text, area_id, per_page=5):
    """
    Отправляет GET-запрос к API hh.ru и получает вакансии.

    search_text - что ищем
    area_id - id региона (2 = Санкт-Петербург)
    per_page - сколько вакансий показать
    """

    url = "https://api.hh.ru/vacancies"

    params = {
        "text": search_text,
        "area": area_id,
        "per_page": per_page
    }

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/18.4 Safari/605.1.15"
        ),
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return data.get("items", [])
        else:
            print("Ошибка при запросе к API.")
            print("Код ошибки:", response.status_code)
            print("Ответ сервера:", response.text)
            return []

    except requests.exceptions.RequestException as error:
        print("Ошибка сети:", error)
        return []


# ---------------------------------------------------------
# ФУНКЦИЯ ДЛЯ ВЫВОДА ИНФОРМАЦИИ О ВАКАНСИИ
# ---------------------------------------------------------
def print_vacancy_info(vacancies):
    """
    Выводит 7 полей по каждой вакансии:
    1. Название
    2. Компания
    3. Город
    4. Зарплата от
    5. Зарплата до
    6. Валюта
    7. Ссылка
    """

    if not vacancies:
        print("Вакансии не найдены.")
        return

    for index, vacancy in enumerate(vacancies, start=1):
        name = vacancy.get("name", "Не указано")
        employer = vacancy.get("employer", {}).get("name", "Не указано")
        city = vacancy.get("area", {}).get("name", "Не указано")

        salary = vacancy.get("salary")
        if salary:
            salary_from = salary.get("from", "Не указано")
            salary_to = salary.get("to", "Не указано")
            currency = salary.get("currency", "Не указано")
        else:
            salary_from = "Не указано"
            salary_to = "Не указано"
            currency = "Не указано"

        vacancy_url = vacancy.get("alternate_url", "Не указано")

        print(f"\nВакансия №{index}")
        print("-" * 40)
        print(f"Название: {name}")
        print(f"Компания: {employer}")
        print(f"Город: {city}")
        print(f"Зарплата от: {salary_from}")
        print(f"Зарплата до: {salary_to}")
        print(f"Валюта: {currency}")
        print(f"Ссылка: {vacancy_url}")


# ---------------------------------------------------------
# ОСНОВНАЯ ЧАСТЬ ПРОГРАММЫ
# ---------------------------------------------------------
def main():
    search_text = "Python"
    area_id = 2   # Санкт-Петербург

    vacancies = get_vacancies(search_text, area_id, per_page=5)
    print_vacancy_info(vacancies)


# ---------------------------------------------------------
# ЗАПУСК ПРОГРАММЫ
# ---------------------------------------------------------
if __name__ == "__main__":
    main()