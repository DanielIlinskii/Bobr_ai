import requests
# from config import open_weather_api_token


# open_weather_api = open_weather_api_token


def get_weather(city, API_key):
    request = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ru&appid={API_key}'
    )

    response = request.json()

    # temp = response['main']['temp']
    # temp_feels_like = response['main']['feels_like']
    # weather = response['weather'][0]['description']
    # humidity = response['main']['humidity']
    # wind = response['wind']['speed']

    return response
