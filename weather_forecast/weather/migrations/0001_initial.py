# Generated by Django 4.2.6 on 2023-10-11 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherForecast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='город')),
                ('time', models.DateTimeField(blank=True, null=True, verbose_name=' Время')),
                ('temperature', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Температура')),
                ('pressure', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='давление')),
                ('wind_speed', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='скорость ветра')),
            ],
            options={
                'verbose_name': 'Прогноз погоды',
                'verbose_name_plural': 'Прогнозы погоды',
            },
        ),
    ]
