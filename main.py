import requests
import json

API_KEY = "43c219af19622859004a0aa84f88fabf"
CITY = "Санкт-Петербург"

#Формируем запрос
url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=ru"

try:
    #Отправляем запрос и получаем ответ
    response = requests.get(url)
    data = json.loads(response.text)
    
    if data["cod"] == 200:
        #Нужные данные
        weather_main = data["weather"][0]["main"]
        weather_desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        feels_like = data["main"]["feels_like"]
        wind_speed = data["wind"]["speed"]
        
        #Вывод информации
        print(f"Погода в городе: {CITY}")
        print("=" * 30)
        print(f"Состояние: {weather_main} ({weather_desc})")
        print(f"Температура: {temp}°C (ощущается как {feels_like}°C)")
        print(f"Влажность: {humidity}%")
        print(f"Давление: {pressure} гПа")
        print(f"Скорость ветра: {wind_speed} м/с")
    else:
        print(f"Ошибка: {data.get('message', 'Неизвестная ошибка')}")
        
except requests.exceptions.RequestException as e:
    print(f"Ошибка подключения: {e}")
except KeyError as e:
    print(f"Ошибка в структуре данных: {e}")
