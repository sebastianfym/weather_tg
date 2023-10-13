# Установка
1. откройте терминал и перейдите в папку для проекта: cd <название директории в которой будет проект>
2. скачайте проект с github: git clone https://github.com/sebastianfym/weather_tg.git
3. перейдите в папку проекта: cd weather_forecast
4. установите venv и активируйте его (в директории с проектом python3 -m venv venv, а затем source venv/bin/activate)
5. установите необходимые библиотеки командой: pip install -r requirements.txt
6. запустите в (разных терминалах или в nohup) сперва django проект, а затем бота:
   python manage.py runserver (запуск Django сервера), а следом python bot/bot.py (запуск бота)
7. запуск тестов: python manage.py test (нужно находиться в корневой директории проекта)

## Описание процессов:
Вы можете делать запросы как через бота (@bogdanweatherforecastbot), так и через браузер, postman и прочие виды интерфейсов

Пример запроса не через бота: http://127.0.0.1:8000/weather/?city=Санкт-Петербург
Вместо "Санкт-Петербург" нужно и можно подставить любой другой город


### Полезные ссылки:
http://127.0.0.1:8000/weather/?city=Москва --- get запрос 
@bogdanweatherforecastbot --- ТГ бот, которого вы запустите
# Приятного пользования
