import requests


# ---------------------------------------------------------
# НАСТРОЙКИ ПРОГРАММЫ
# ---------------------------------------------------------

API_KEY = "43c219af19622859004a0aa84f88fabf"

city_name = "Saint-Petersburg"


# ---------------------------------------------------------
# ФУНКЦИЯ ПОЛУЧЕНИЯ КООРДИНАТ ГОРОДА
# ---------------------------------------------------------
def get_city_coordinates(city, api_key):
    """
    Получает координаты города по его названию.

    Аргументы:
    city -- название города
    api_key -- API-ключ OpenWeather

    Возвращает:
    кортеж (lat, lon, country, real_city_name)
    или None, если город не найден
    """

    url = "http://api.openweathermap.org/geo/1.0/direct"

    params = {
        "q": city,       # название города
        "limit": 1,      # берем только первый найденный вариант
        "appid": api_key
    }

    response = requests.get(url, params=params)

    # Если запрос не удался, выводим ошибку
    if response.status_code != 200:
        print("Ошибка при получении координат.")
        print("Код ошибки:", response.status_code)
        return None

    data = response.json()

    # Если список пустой, значит город не найден
    if not data:
        print("Город не найден.")
        return None

    # Берем первый результат
    city_data = data[0]

    lat = city_data["lat"]
    lon = city_data["lon"]
    country = city_data.get("country", "Не указано")
    real_city_name = city_data.get("name", city)

    return lat, lon, country, real_city_name


# ---------------------------------------------------------
# ФУНКЦИЯ ПОЛУЧЕНИЯ ПОГОДЫ ПО КООРДИНАТАМ
# ---------------------------------------------------------
def get_weather(lat, lon, api_key):
    """
    Получает текущую погоду по координатам.

    Аргументы:
    lat -- широта
    lon -- долгота
    api_key -- API-ключ OpenWeather

    Возвращает:
    JSON-ответ с погодой или None при ошибке
    """

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric",   # температура в градусах Цельсия
        "lang": "ru"         # описание погоды на русском
    }

    response = requests.get(url, params=params)

    # Проверка успешности запроса
    if response.status_code != 200:
        print("Ошибка при получении погоды.")
        print("Код ошибки:", response.status_code)
        return None

    return response.json()


# ---------------------------------------------------------
# ФУНКЦИЯ ВЫВОДА РЕЗУЛЬТАТА
# ---------------------------------------------------------
def print_weather_info(weather_data, city, country):
    """
    Красиво выводит информацию о погоде.

    Выводимые поля:
    1. Город
    2. Страна
    3. Температура
    4. Ощущается как
    5. Описание погоды
    6. Влажность
    7. Давление
    """

    # Извлекаем нужные данные из JSON
    temperature = weather_data["main"]["temp"]
    feels_like = weather_data["main"]["feels_like"]
    humidity = weather_data["main"]["humidity"]
    pressure = weather_data["main"]["pressure"]
    description = weather_data["weather"][0]["description"]

    # Структурированный вывод
    print("\nТЕКУЩАЯ ПОГОДА")
    print("-" * 35)
    print(f"Город: {city}")
    print(f"Страна: {country}")
    print(f"Температура: {temperature} °C")
    print(f"Ощущается как: {feels_like} °C")
    print(f"Описание: {description}")
    print(f"Влажность: {humidity} %")
    print(f"Давление: {pressure} гПа")


# ---------------------------------------------------------
# ОСНОВНАЯ ЧАСТЬ ПРОГРАММЫ
# ---------------------------------------------------------
def main():
    """
    Основная функция:
    1. Получает координаты города
    2. Получает погоду
    3. Выводит результат
    """

    # Проверяем, указан ли API-ключ
    if API_KEY == "API_КЛЮЧ":
        print("Сначала вставьте свой API-ключ в переменную API_KEY.")
        return

    # Получаем координаты города
    coordinates = get_city_coordinates(city_name, API_KEY)

    # Если координаты не получены, завершаем программу
    if coordinates is None:
        return

    lat, lon, country, real_city_name = coordinates

    # Получаем погоду по координатам
    weather_data = get_weather(lat, lon, API_KEY)

    # Если погода не получена, завершаем программу
    if weather_data is None:
        return

    # Выводим результат
    print_weather_info(weather_data, real_city_name, country)


# ---------------------------------------------------------
# ЗАПУСК ПРОГРАММЫ
# ---------------------------------------------------------
if __name__ == "__main__":
    main()