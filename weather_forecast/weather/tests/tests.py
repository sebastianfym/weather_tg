import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_forecast.config.settings')
django.setup()

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from datetime import datetime
import pytz

from weather.models import WeatherForecast


class WeatherDataViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.forecast_time_zone = pytz.timezone('Europe/Moscow')
        self.current_time = datetime(2023, 10, 12, 12, 0, 0, tzinfo=self.forecast_time_zone)
        self.city_name = "Moscow"
        self.latitude = 55.7558
        self.longitude = 37.6176


    def test_get_weather_data_created(self):
        # Проверка, что представление создает запись, если ее нет
        url = reverse('weather-data-list')
        response = self.client.get(url, {'city': self.city_name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        weather_data = WeatherForecast.objects.get(city_name=self.city_name)
        self.assertEqual(weather_data.city_name, self.city_name)

    def test_get_weather_data_updated(self):
        # Проверка, что представление обновляет запись, если она уже существует
        WeatherForecast.objects.create(city_name=self.city_name, time=self.current_time, temperature=15.0, pressure=765.0, wind_speed=5.0)
        url = reverse('weather-data-list')
        response = self.client.get(url, {'city': self.city_name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        weather_data = WeatherForecast.objects.get(city_name=self.city_name)
        self.assertNotEqual(weather_data.time, self.current_time)


    def test_create_weather_data(self):
        url = reverse('weather-data-list')
        data = {
            'city_name': self.city_name,
            'latitude': self.latitude,
            'longitude': self.longitude,
            # Add other required fields here
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        weather_data = WeatherForecast.objects.get(city_name=self.city_name)
        self.assertEqual(weather_data.city_name, self.city_name)

    def test_retrieve_weather_data(self):
        weather_data = WeatherForecast.objects.create(
            city_name=self.city_name,
            temperature = 7.00,
            pressure = 740.00,
            wind_speed =9.60
        )
        url = reverse('weather-data-detail', kwargs={'pk': weather_data.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['city_name'], self.city_name)

    def test_update_weather_data(self):
        weather_data = WeatherForecast.objects.create(
            city_name=self.city_name,
            temperature=7.00,
            pressure=740.00,
            wind_speed=9.60

        )
        updated_city_name = "Updated City"
        url = reverse('weather-data-detail', kwargs={'pk': weather_data.pk})
        data = {
            'city_name': updated_city_name,
            # Add other updated fields here
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        weather_data.refresh_from_db()
        self.assertEqual(weather_data.city_name, updated_city_name)

    def test_delete_weather_data(self):
        weather_data = WeatherForecast.objects.create(
            city_name=self.city_name,
            temperature=7.00,
            pressure=740.00,
            wind_speed=9.60

        )
        url = reverse('weather-data-detail', kwargs={'pk': weather_data.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(WeatherForecast.objects.filter(pk=weather_data.pk).exists())

