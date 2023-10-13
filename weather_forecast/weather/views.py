import pytz
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import WeatherForecast
from .serializers import WeatherForecastSerializer

from .service import get_weather_forecast, get_geolocation


class WeatherDataViewSet(viewsets.ModelViewSet):
    queryset = WeatherForecast.objects.all()
    serializer_class = WeatherForecastSerializer

    def list(self, request):
        forecast_time_zone = pytz.timezone('Europe/Moscow')
        current_time = timezone.now().astimezone(forecast_time_zone)

        city_name = request.query_params.get("city")

        try:
            latitude, longitude = get_geolocation(city_name)
        except ValueError:
            return Response({"error": "Я не смог найти погоду в Вашем городе."}, status=status.HTTP_400_BAD_REQUEST)

        weather_forecast, created = WeatherForecast.objects.get_or_create(city_name=city_name)

        try:
            time_difference = current_time - weather_forecast.time
        except TypeError:
            created = True

        if created or time_difference.total_seconds() > 30 * 60:
            response = get_weather_forecast(latitude, longitude)
            try:
                if response.status_code == 200:
                    data = response.json()

                    weather_forecast.temperature = data['fact']['temp']
                    weather_forecast.pressure = data['fact']['pressure_mm']
                    weather_forecast.wind_speed = data['fact']['wind_speed']
                    weather_forecast.time = current_time
                    weather_forecast.save()
                    return Response({"weather": self.serializer_class(weather_forecast).data})

                else:
                    fact = "Я не смог найти погоду в Вашем городе."
                    return Response({'error': fact}, status=status.HTTP_400_BAD_REQUEST)
            except AttributeError:
                fact = "Проверьте название Вашего города."
                return Response({'error': fact}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"weather": self.serializer_class(weather_forecast).data})


