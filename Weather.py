import requests
from flask import Flask, request, render_template, session, redirect, url_for
from pprint import pprint
from config import open_weather_token

def get_weather(city, open_weather_token):
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        # pprint(data)
        city = data["name"]
        cur_weather = data["main"]["temp"]
        print(f"Погода в городе: {city}\n Температура: {cur_weather}*C")

    except Exception as ex:
        print(ex)
        print("Проверьте название города")

def main():
    # city = input("Введите город:") Можно менять город
    city = "Астана"
    get_weather(city, open_weather_token)

if __name__ == '__main__':
    main()


# headers = {
#     'X-RapidAPI-Host': 'weatherapi-com.p.rapidapi.com',
#     'X-RapidAPI-Key': 'your_api_key'
# }

# response = requests.get("https://weatherapi-com.p.rapidapi.com/current.json", headers=headers)

# print(response.headers)
# print(response.content)
# print(response.status_code)

# e616a01b1c14b251d15716e7557287cb
