from django.db import models


class WeatherForecast(models.Model):
    city_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='город')
    time = models.DateTimeField(blank=True, null=True, verbose_name=' Время')
    temperature = models.DecimalField(max_digits=5, blank=True, null=True, decimal_places=2, verbose_name='Температура')
    pressure = models.DecimalField(max_digits=5, blank=True, null=True, decimal_places=2, verbose_name='давление')
    wind_speed = models.DecimalField(max_digits=5, blank=True, null=True, decimal_places=2, verbose_name='скорость ветра')

    def __str__(self):
        return f"{self.city_name} {self.time} {self.temperature} {self.pressure} {self.wind_speed}"

    class Meta:
        verbose_name = 'Прогноз погоды'
        verbose_name_plural = 'Прогнозы погоды'
        app_label = 'weather'