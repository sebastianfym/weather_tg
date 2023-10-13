from django.contrib import admin

from .models import WeatherForecast


# @admin.site.register(WeatherForecast)
class WeatherForecastAdmin(admin.ModelAdmin):
    list_display = ('city_name', 'time', 'temperature', 'pressure', 'wind_speed')


admin.site.register(WeatherForecast, WeatherForecastAdmin)

