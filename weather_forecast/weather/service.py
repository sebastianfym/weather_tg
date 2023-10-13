import requests
from geopy import Nominatim

weather_api_key = 'a355be95-8f31-4640-8117-d95d6094f078'


def get_geolocation(city_name):
    geolocator = Nominatim(user_agent="myGeocoder")

    location = geolocator.geocode(city_name)

    if location:
        latitude = location.latitude
        longitude = location.longitude
        return latitude, longitude
    else:
        return "Я не смог найти погоду в Вашем городе."

def get_weather_forecast(latitude, longitude):

    url = f"https://api.weather.yandex.ru/v2/forecast?lat={latitude}&lon={longitude}&lang=ru_RU"

    headers = {
        'X-Yandex-API-Key': weather_api_key
    }

    response = requests.get(url, headers=headers)
    return response