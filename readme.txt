Добрый день!
Надеюсь вы это читаете в верной кодировке.
Инструкция по запуску Квалификационного задания для разработчиков Python от FunBox.

Сначала довесок к теоретической части. 
Ниже пример функционального программирования на python.
тоже выложен на github:

Functional Programming Example

запуск приложения:
python check_factorial.py

Для выполнения основного задания прежде всего на машине потребуется поставить
redis. За пути достижения этого на Windows/MacOS поручится не могу, все нижеследующее
сделано в WSL для Windows, оно же 
Distributor ID: Ubuntu
Description:    Ubuntu 20.04.2 LTS
Release:        20.04
Codename:       focal

устанавливаем утилиты для работы с БД:
sudo apt install redis-tools

устанавливаем сервер для обработки запросов:
sudo apt install redis-server

Для демонстрации результатов работы приложения по задаче FunBox требуется
выполнение запросов к серверу. Наиболее просто вариант - использовать программу curl,
входящую в состав всех дистрибутивов linux. При работе с версия Windows/MacOS возможны
проблемы с пониманием синтаксиса в командной строке.

По реализации задания в фреймворке FLASK.
Python FLASK implimentation of task

Для корректной работы приложения рекомендуется установить отдельную виртуальную среду.
Например, flasksample, при помощи команды:

virtualenv flasksample

Далее активируем среду в командной строке:
source flasksample/bin/activate

В среде устанавливаем необходимые библиотеки для работы:

pip install Flask redis
pip install -r flask_requirements.txt

После успешной установки запускаем приложение:
python app_track_v_flask.py

Для работы с POST запросом командой curl, необходимо дать следующую команду (копируйте всю строку отсюда):

curl -X POST http://127.0.0.1:5000/visited_links -H "Content-Type: application/json" -d '{"links": ["https://ya.ru", "https://ya.ru?q=123", "funbox.ru", "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"]}'

Приложение должно ответить в соответствии с заданием.

Для работы с GET запросом командой curl, необходимо дать следующую команду (копируйте всю строку отсюда):

curl -X GET "http://127.0.0.1:5000/visited_domains?from=0&to=9999999999"

Приложение должно ответить в соответствии с изложенным заданием.

По реализации задания в фреймворке FLASK
Python FASTAPI implimentation of task


Для корректной работы приложения рекомендуется установить отдельную виртуальную среду.
Например, fastapisample, при помощи команды:

pip install fastapi
pip install redis
pip install -r fastapi_requirements.txt

После успешной установки запускаем приложение:
python app_track_v_fastapi.py

Для работы с POST запросом командой curl, необходимо дать следующую команду (копируйте всю строку отсюда):

curl -X POST http://127.0.0.1:8000/visited_links -H "Content-Type: application/json" -d '{"links": ["https://ya.ru", "https://ya.ru?q=123", "funbox.ru", "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"]}'

Обратите внимание, в отличии от реализации FLASK данная реализация работает не на порту 5000, а на порту 8000. Таким образом, если желаете,
можно запускать оба решения одновременно и делать запросы к одной и той же базе.

Для работы с GET запросом командой curl, необходимо дать следующую команду (копируйте всю строку отсюда, порт работы приложения также 8000):

curl -X GET "http://127.0.0.1:8000/visited_domains?from=0&to=9999999999"


Благодарю за внимание.
С уважением,
ДК
14.04.2023